from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from django.contrib.auth import get_user_model
from .models import Deal, DealAnalytics, UserBehavior, DealAlert, Notification
from .serializers import DealSerializer, CategorySerializer, DealAlertSerializer, NotificationSerializer
from merchants.models import Category, PageAdvert
import json
from datetime import timedelta

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.filter(status='active')
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'end_datetime', 'discount_price', 'views_count', 'purchases_count']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get query parameters - handle both DRF and Django requests
        if hasattr(self.request, 'query_params'):
            # DRF request
            query_params = self.request.query_params
        else:
            # Django request
            query_params = self.request.GET
        
        category = query_params.get('category', None)
        merchant = query_params.get('merchant', None)
        deal_type = query_params.get('deal_type', None)
        urgency_level = query_params.get('urgency_level', None)
        price_min = query_params.get('price_min', None)
        price_max = query_params.get('price_max', None)
        trending = query_params.get('trending', None)
        flash_sale = query_params.get('flash_sale', None)
        
        if category:
            queryset = queryset.filter(category_id=category)
        if merchant:
            queryset = queryset.filter(merchant_id=merchant)
        if deal_type:
            queryset = queryset.filter(deal_type=deal_type)
        if urgency_level:
            queryset = queryset.filter(urgency_level=urgency_level)
        if price_min:
            queryset = queryset.filter(discount_price__gte=price_min)
        if price_max:
            queryset = queryset.filter(discount_price__lte=price_max)
        if trending:
            queryset = queryset.filter(is_trending=True)
        if flash_sale:
            queryset = queryset.filter(is_flash_sale=True)
            
        return queryset.filter(
            start_datetime__lte=timezone.now(),
            end_datetime__gte=timezone.now()
        )

    def retrieve(self, request, *args, **kwargs):
        """Track deal view when retrieving individual deal"""
        instance = self.get_object()
        
        # Track view
        instance.views_count += 1
        instance.save()
        
        # Track user behavior if user is authenticated
        if request.user.is_authenticated:
            UserBehavior.objects.create(
                user=request.user,
                deal=instance,
                action='view',
                session_id=request.session.session_key or '',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        # Update daily analytics
        analytics, created = DealAnalytics.objects.get_or_create(
            deal=instance,
            date=timezone.now().date()
        )
        analytics.views += 1
        analytics.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_deals = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_deals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        expiring_deals = self.get_queryset().order_by('end_datetime')[:6]
        serializer = self.get_serializer(expiring_deals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        trending_deals = self.get_queryset().filter(is_trending=True)[:6]
        serializer = self.get_serializer(trending_deals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def flash_sales(self, request):
        flash_deals = self.get_queryset().filter(is_flash_sale=True)[:6]
        serializer = self.get_serializer(flash_deals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def track_click(self, request, pk=None):
        """Track when user clicks on a deal"""
        deal = self.get_object()
        deal.clicks_count += 1
        deal.save()
        
        if request.user.is_authenticated:
            UserBehavior.objects.create(
                user=request.user,
                deal=deal,
                action='click',
                session_id=request.session.session_key or '',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        # Update daily analytics
        analytics, created = DealAnalytics.objects.get_or_create(
            deal=deal,
            date=timezone.now().date()
        )
        analytics.clicks += 1
        analytics.save()
        
        return Response({'status': 'click tracked'})

    @action(detail=True, methods=['post'])
    def save_deal(self, request, pk=None):
        """Save deal to user's wishlist"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        deal = self.get_object()
        UserBehavior.objects.create(
            user=request.user,
            deal=deal,
            action='save',
            session_id=request.session.session_key or '',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'status': 'deal saved'})

    @action(detail=True, methods=['post'])
    def share_deal(self, request, pk=None):
        """Track deal sharing"""
        deal = self.get_object()
        
        if request.user.is_authenticated:
            UserBehavior.objects.create(
                user=request.user,
                deal=deal,
                action='share',
                session_id=request.session.session_key or '',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return Response({'status': 'share tracked'})

class DealAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for managing deal alerts"""
    serializer_class = DealAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DealAlert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for managing notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all marked as read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})

def deals_page(request):
    # Get active deals
    active_deals = Deal.objects.filter(
        status='active',
        start_datetime__lte=timezone.now(),
        end_datetime__gte=timezone.now()
    ).order_by('-created_at')
    
    # Get all categories for the filter
    categories = Category.objects.all()
    
    # Get the selected category from query params
    category_id = request.GET.get('category')
    advert = None
    if category_id:
        active_deals = active_deals.filter(category_id=category_id)
        category_obj = Category.objects.get(id=category_id)
        category_name = category_obj.name
        advert = PageAdvert.objects.filter(page_type='category', category=category_obj, is_active=True).order_by('-updated_at').first()
    else:
        category_name = None
        advert = PageAdvert.objects.filter(page_type='category', category__isnull=True, is_active=True).order_by('-updated_at').first()
    
    context = {
        'deals': active_deals,
        'categories': categories,
        'category_name': category_name,
        'total_results': active_deals.count(),
        'advert': advert
    }
    return render(request, 'deal_list.html', context)

def deal_detail(request, slug):
    """View for individual deal detail page"""
    # Try to find the deal by slug first, then by ID if slug is numeric
    try:
        if slug.isdigit():
            # If slug is a number, treat it as an ID
            deal = get_object_or_404(Deal, id=slug, status='active')
        else:
            # Otherwise treat it as a slug
            deal = get_object_or_404(Deal, slug=slug, status='active')
    except Deal.DoesNotExist:
        # If not found, try to find by ID regardless
        try:
            deal = get_object_or_404(Deal, id=slug)
        except (ValueError, Deal.DoesNotExist):
            # If still not found, return 404
            from django.http import Http404
            raise Http404("Deal not found")
    
    # Check if deal is currently active
    now = timezone.now()
    if deal.start_datetime > now or deal.end_datetime < now:
        # Deal is not currently active
        context = {
            'deal': deal,
            'is_expired': deal.end_datetime < now,
            'is_not_started': deal.start_datetime > now,
        }
        return render(request, 'deal_detail_inactive.html', context)
    
    # Get related deals from the same merchant
    related_deals = Deal.objects.filter(
        merchant=deal.merchant,
        status='active',
        start_datetime__lte=now,
        end_datetime__gte=now
    ).exclude(id=deal.id)[:3]
    
    context = {
        'deal': deal,
        'related_deals': related_deals,
    }
    return render(request, 'deal_detail.html', context)
