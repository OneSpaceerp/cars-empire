from django.shortcuts import render, get_object_or_404
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
from django.db import transaction
from .models import Coupon, PromoCode, Redemption, CouponEvent, WorkOrder
from .serializers import (
    CouponSerializer, PromoCodeSerializer, 
    RedemptionSerializer, WorkOrderSerializer
)
from merchants.models import Merchant, Branch

class CouponListView(generics.ListCreateAPIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['coupon_code', 'deal__title', 'merchant__name']
    ordering_fields = ['created_at', 'valid_until']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Coupon.objects.all()
        # Return vouchers purchased by this user
        return Coupon.objects.filter(user=user)

class CouponDetailView(generics.RetrieveAPIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Coupon.objects.all()
        return Coupon.objects.filter(user=user)

class MerchantCouponValidateView(APIView):
    """
    PRD Section 17.9: Non-destructive, read-only coupon verification.
    Merchant cashiers call this when scanning QR or entering code.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('coupon_code') or request.data.get('code')
        qr_token = request.data.get('qr_token')
        branch_id = request.data.get('branch_id')

        if not code and not qr_token:
            return Response(
                {'error': 'Either coupon_code or qr_token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if qr_token:
                coupon = Coupon.objects.get(qr_token=qr_token)
            else:
                normalized = code.strip().upper()
                coupon = Coupon.objects.filter(coupon_code__iexact=normalized).first()
                if not coupon:
                    # Also try searching without dashes
                    clean_code = normalized.replace('-', '')
                    coupon = Coupon.objects.filter(coupon_code__icontains=clean_code).first()

            if not coupon:
                return Response(
                    {'valid': False, 'error': 'COUPON_NOT_FOUND', 'message': 'Coupon code does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check status
            if coupon.status == 'redeemed':
                return Response({
                    'valid': False,
                    'error': 'ALREADY_REDEEMED',
                    'message': f'This coupon was already redeemed on {coupon.redemption_datetime.strftime("%Y-%m-%d %H:%M") if coupon.redemption_datetime else "earlier"}.',
                    'coupon_id': coupon.id,
                    'coupon_code': coupon.coupon_code
                }, status=status.HTTP_400_BAD_REQUEST)

            if not coupon.is_valid():
                return Response({
                    'valid': False,
                    'error': 'EXPIRED_OR_INACTIVE',
                    'message': 'Coupon has expired or is not yet active.',
                    'valid_from': coupon.valid_from,
                    'valid_until': coupon.valid_until
                }, status=status.HTTP_400_BAD_REQUEST)

            # Audit lookup event
            CouponEvent.objects.create(
                coupon=coupon,
                event_type='validated',
                actor=request.user,
                notes=f"Validated by staff {request.user.username}"
            )

            # Format vehicle info if attached
            vehicle_info = None
            if coupon.vehicle:
                vehicle_info = {
                    'make': coupon.vehicle.make.name if coupon.vehicle.make else '',
                    'model': coupon.vehicle.model.name if coupon.vehicle.model else '',
                    'year': coupon.vehicle.year,
                    'plate': coupon.vehicle.license_plate
                }

            return Response({
                'valid': True,
                'coupon_id': coupon.id,
                'coupon_code': coupon.coupon_code,
                'offer': {
                    'id': coupon.deal.id,
                    'title': coupon.deal.title,
                    'original_price': coupon.deal.original_price,
                    'discount_price': coupon.deal.discount_price,
                },
                'merchant': {
                    'id': coupon.merchant.id if coupon.merchant else None,
                    'name': coupon.merchant.name if coupon.merchant else '',
                },
                'customer': {
                    'display_name': coupon.user.get_full_name() or coupon.user.username,
                },
                'vehicle': vehicle_info,
                'valid_until': coupon.valid_until,
                'terms': coupon.deal.terms_and_conditions if hasattr(coupon.deal, 'terms_and_conditions') else ''
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MerchantCouponRedeemView(APIView):
    """
    PRD Section 17.9 & 17.10: Atomic, concurrency-safe coupon redemption.
    Uses SELECT ... FOR UPDATE to guarantee double-redemption immunity.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        coupon_id = request.data.get('coupon_id')
        code = request.data.get('coupon_code') or request.data.get('code')
        qr_token = request.data.get('qr_token')
        branch_id = request.data.get('branch_id')
        device_id = request.data.get('device_id', '')
        method = request.data.get('method', 'qr_scan')
        notes = request.data.get('notes', '')

        if not coupon_id and not code and not qr_token:
            return Response(
                {'error': 'A coupon identifier (coupon_id, coupon_code, or qr_token) is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Acquire row-level lock (PRD Section 17.10)
                queryset = Coupon.objects.select_for_update()
                if coupon_id:
                    coupon = queryset.get(id=coupon_id)
                elif qr_token:
                    coupon = queryset.get(qr_token=qr_token)
                else:
                    normalized = code.strip().upper()
                    coupon = queryset.filter(coupon_code__iexact=normalized).first()
                    if not coupon:
                        return Response(
                            {'error': 'COUPON_NOT_FOUND', 'message': 'Coupon code does not exist.'},
                            status=status.HTTP_404_NOT_FOUND
                        )

                # Check if already redeemed
                if coupon.status == 'redeemed':
                    return Response({
                        'error': 'ALREADY_REDEEMED',
                        'message': f'This coupon was already redeemed on {coupon.redemption_datetime.strftime("%Y-%m-%d %H:%M") if coupon.redemption_datetime else "earlier"}.'
                    }, status=status.HTTP_409_CONFLICT)

                if not coupon.is_valid():
                    return Response({
                        'error': 'INVALID_STATE',
                        'message': 'Coupon is not active or has expired.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Identify branch if provided
                branch = None
                if branch_id:
                    branch = Branch.objects.filter(id=branch_id).first()
                elif coupon.branch:
                    branch = coupon.branch

                # Transition Coupon State
                now = timezone.now()
                coupon.status = 'redeemed'
                coupon.redemption_datetime = now
                coupon.redeemed_at = now
                coupon.redeemed_by_staff = request.user
                coupon.save()

                # Create Redemption Record
                merchant = coupon.merchant or (coupon.deal.merchant if coupon.deal else None)
                redemption = Redemption.objects.create(
                    coupon=coupon,
                    merchant=merchant,
                    branch=branch,
                    staff_user=request.user,
                    device_fingerprint=device_id,
                    redeemed_at=now,
                    method=method,
                    notes=notes,
                    status='completed'
                )

                # Create Work Order (PRD Section 2.9 & 17.3)
                work_order = WorkOrder.objects.create(
                    coupon=coupon,
                    redemption=redemption,
                    merchant=merchant,
                    branch=branch,
                    vehicle=coupon.vehicle,
                    customer=coupon.user,
                    technician=request.user,
                    status='opened',
                    started_at=now
                )

                # Log Coupon Audit Event
                CouponEvent.objects.create(
                    coupon=coupon,
                    event_type='redeemed',
                    actor=request.user,
                    branch=branch,
                    notes=f"Redeemed via {method}. Receipt #{redemption.receipt_number}"
                )

                return Response({
                    'success': True,
                    'status': 'redeemed',
                    'receipt_number': redemption.receipt_number,
                    'redemption_id': redemption.id,
                    'redeemed_at': redemption.redeemed_at,
                    'work_order_id': work_order.id,
                    'work_order_number': work_order.work_order_number,
                    'customer_name': coupon.user.get_full_name() or coupon.user.username,
                    'deal_title': coupon.deal.title,
                    'amount': coupon.deal.discount_price
                }, status=status.HTTP_201_CREATED)

        except Coupon.DoesNotExist:
            return Response({'error': 'Coupon not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MerchantRecentRedemptionsView(APIView):
    """
    Returns recent redemptions for the authenticated merchant's dashboard.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        redemptions = Redemption.objects.all()[:20]
        serializer = RedemptionSerializer(redemptions, many=True)
        return Response({'redemptions': serializer.data})

class PromoCodeValidateView(APIView):
    """
    Validate marketing promo/discount codes at checkout (e.g. WELCOME10).
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        code = request.data.get('code', '').strip()
        cart_total = float(request.data.get('cart_total', 0))

        try:
            promo = PromoCode.objects.get(code__iexact=code)
            if not promo.is_valid():
                return Response({'valid': False, 'error': 'Promo code is expired or inactive.'}, status=400)

            if promo.min_purchase and cart_total < float(promo.min_purchase):
                return Response({
                    'valid': False, 
                    'error': f'Minimum purchase of {promo.min_purchase} EGP required.'
                }, status=400)

            discount = 0
            if promo.discount_type == 'percentage':
                discount = cart_total * (float(promo.discount_value) / 100.0)
                if promo.max_discount and discount > float(promo.max_discount):
                    discount = float(promo.max_discount)
            else:
                discount = float(promo.discount_value)

            return Response({
                'valid': True,
                'code': promo.code,
                'discount_amount': round(discount, 2),
                'discount_type': promo.discount_type,
                'discount_value': promo.discount_value
            })
        except PromoCode.DoesNotExist:
            return Response({'valid': False, 'error': 'Invalid promo code.'}, status=404)

