from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from deals.models import Deal

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response(
                {'error': 'Item ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = cart.items.get(id=item_id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        if not item_id or not quantity:
            return Response(
                {'error': 'Item ID and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = cart.items.get(id=item_id)
            item.quantity = quantity
            item.save()
            return Response(CartItemSerializer(item).data)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        deal_id = request.data.get('deal_id')
        merchant_id = request.data.get('merchant_id')
        quantity = int(request.data.get('quantity', 1))
        # Optionally support service_id in the future
        if deal_id:
            try:
                deal = Deal.objects.get(id=deal_id)
            except Deal.DoesNotExist:
                return Response({'error': 'Deal not found.'}, status=status.HTTP_404_NOT_FOUND)
            merchant = deal.merchant if hasattr(deal, 'merchant') else None
            if not merchant and not merchant_id:
                return Response({'error': 'Merchant is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if not merchant:
                from merchants.models import Merchant
                try:
                    merchant = Merchant.objects.get(id=merchant_id)
                except Merchant.DoesNotExist:
                    return Response({'error': 'Merchant not found.'}, status=status.HTTP_404_NOT_FOUND)
            # Use get_or_create to avoid duplicate entries
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                merchant=merchant,
                deal=deal,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            # Return the full cart after adding an item
            return Response(CartSerializer(cart, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response({'error': 'deal_id is required.'}, status=status.HTTP_400_BAD_REQUEST) 