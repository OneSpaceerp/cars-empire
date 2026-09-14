from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.db.models import F, FloatField, ExpressionWrapper, Q
from math import radians, cos, sin, asin, sqrt
from .models import Merchant, Category, Branch, MerchantUser, MerchantImage, PageAdvert
from .serializers import (
    MerchantSerializer, CategorySerializer,
    BranchSerializer, MerchantUserSerializer,
    MerchantImageSerializer
)
from .permissions import IsMerchantOwnerOrReadOnly
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import json
from django.utils.encoding import force_str
import logging
from users.models import Vehicle
from django.db import models
from deals.models import Deal

logger = logging.getLogger(__name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

class NearbyMerchantsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            lat = request.query_params.get('lat')
            lng = request.query_params.get('lng')
            radius = request.query_params.get('radius', 50)  # Default 50km
            category_slug = request.query_params.get('category')
            logger.debug(f"[NearbyMerchantsView] Params: lat={lat}, lng={lng}, radius={radius}, category={category_slug}")
            if not lat or not lng:
                logger.warning("[NearbyMerchantsView] Missing latitude or longitude.")
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
            try:
                lat = float(lat)
                lng = float(lng)
                radius = float(radius)
            except (ValueError, TypeError):
                logger.warning("[NearbyMerchantsView] Invalid latitude, longitude, or radius values.")
                return JsonResponse({'error': 'Invalid latitude, longitude, or radius values'}, status=400)

            # Find all branches with coordinates
            branches = Branch.objects.filter(latitude__isnull=False, longitude__isnull=False)
            logger.debug(f"[NearbyMerchantsView] Total branches with coordinates: {branches.count()}")
            branch_ids_in_radius = []
            merchant_ids = set()
            for branch in branches:
                try:
                    branch_lat = float(branch.latitude)
                    branch_lng = float(branch.longitude)
                    distance = haversine_distance(lat, lng, branch_lat, branch_lng)
                    if distance <= radius:
                        branch_ids_in_radius.append(branch.id)
                        merchant_ids.add(branch.merchant_id)
                except Exception as e:
                    logger.error(f"[NearbyMerchantsView] Error processing branch {getattr(branch, 'id', '?')}: {e}")
                    continue
            logger.debug(f"[NearbyMerchantsView] Branches within radius: {len(branch_ids_in_radius)}")
            logger.debug(f"[NearbyMerchantsView] Merchant IDs in radius: {merchant_ids}")

            # Filter merchants by category if provided
            merchants = Merchant.objects.filter(id__in=merchant_ids)
            logger.debug(f"[NearbyMerchantsView] Merchants before category filter: {merchants.count()}")
            if category_slug:
                merchants = merchants.filter(categories__slug=category_slug)
                logger.debug(f"[NearbyMerchantsView] Merchants after category filter: {merchants.count()}")

            results = []
            for merchant in merchants:
                all_branches = merchant.branches.all()
                logger.debug(f"[NearbyMerchantsView] Merchant {merchant.id} ({merchant.name}) has {all_branches.count()} branches.")
                serializer = MerchantSerializer(merchant, context={'request': request})
                data = serializer.data
                data['branches'] = BranchSerializer(all_branches, many=True).data
                results.append(data)

            logger.info(f"[NearbyMerchantsView] Returning {len(results)} merchants.")
            return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            logger.error(f"[NearbyMerchantsView] Unexpected error: {e}")
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

# Create your views here.

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsMerchantOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'address_text']
    ordering_fields = ['name', 'rating', 'created_at']
    ordering = ['-rating', '-is_featured', 'name']

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        print("Nearby action called")  # Debug log
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 50)  # Default 50km
        
        print(f"Parameters: lat={lat}, lng={lng}, radius={radius}")  # Debug log
        
        if not lat or not lng:
            return Response(
                {'error': 'Latitude and longitude are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
            
            # Get all merchants with valid coordinates
            merchants = Merchant.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )
            
            print(f"Found {merchants.count()} merchants with valid coordinates")  # Debug log
            
            # Calculate distance and filter by radius
            nearby_merchants = []
            for merchant in merchants:
                distance = haversine_distance(
                    lat, lng,
                    float(merchant.latitude),
                    float(merchant.longitude)
                )
                print(f"Merchant {merchant.name}: distance = {distance:.2f}km")  # Debug log
                if distance <= radius:
                    merchant.distance = distance
                    nearby_merchants.append(merchant)
            
            print(f"Found {len(nearby_merchants)} merchants within {radius}km")  # Debug log
            
            # Sort by distance
            nearby_merchants.sort(key=lambda x: x.distance)
            
            serializer = self.get_serializer(nearby_merchants, many=True)
            return Response(serializer.data)
            
        except (ValueError, TypeError) as e:
            print(f"Error processing request: {str(e)}")  # Debug log
            return Response(
                {'error': 'Invalid latitude, longitude, or radius values'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        queryset = Merchant.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(categories__slug=category)
        
        # Filter by location
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = float(self.request.query_params.get('radius', 10))  # Default 10km
        
        if lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)
                
                # Filter merchants with valid coordinates
                queryset = queryset.filter(
                    latitude__isnull=False,
                    longitude__isnull=False
                )
                
                # Calculate distance for each merchant
                merchants_with_distance = []
                for merchant in queryset:
                    distance = haversine_distance(
                        lat, lng,
                        float(merchant.latitude),
                        float(merchant.longitude)
                    )
                    if distance <= radius:
                        merchant.distance = distance
                        merchants_with_distance.append(merchant)
                
                # Sort by distance
                merchants_with_distance.sort(key=lambda x: x.distance)
                return merchants_with_distance
            except (ValueError, TypeError):
                pass
        
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_merchants = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_merchants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        merchant = self.get_object()
        serializer = MerchantImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=merchant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_image(self, request, pk=None):
        merchant = self.get_object()
        image_id = request.data.get('image_id')
        
        if not image_id:
            return Response(
                {'error': 'Image ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            image = merchant.images.get(id=image_id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MerchantImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='for-vehicle')
    def for_vehicle(self, request):
        """
        Returns merchants that serve the make of the user's vehicle (by vehicle_id),
        or all makes (makes is empty).
        Query param: vehicle_id
        """
        vehicle_id = request.query_params.get('vehicle_id')
        if not vehicle_id:
            return Response({'error': 'vehicle_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id, user=request.user)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        merchants = Merchant.objects.filter(
            models.Q(makes=vehicle.make) | models.Q(makes__isnull=True)
        ).distinct()
        serializer = self.get_serializer(merchants, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsMerchantOwnerOrReadOnly]

    def get_queryset(self):
        merchant_id = self.kwargs.get('merchant_pk')
        if merchant_id:
            return Branch.objects.filter(merchant_id=merchant_id)
        return Branch.objects.all()

class MerchantUserViewSet(viewsets.ModelViewSet):
    queryset = MerchantUser.objects.all()
    serializer_class = MerchantUserSerializer
    permission_classes = [IsAuthenticated, IsMerchantOwnerOrReadOnly]

    def get_queryset(self):
        merchant_id = self.kwargs.get('merchant_pk')
        if merchant_id:
            return MerchantUser.objects.filter(merchant_id=merchant_id)
        return MerchantUser.objects.all()

# Temporarily comment out ServiceViewSet
# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsMerchantOwnerOrReadOnly]
# 
#     def get_queryset(self):
#         merchant_id = self.kwargs.get('merchant_pk')
#         if merchant_id:
#             return Service.objects.filter(merchant_id=merchant_id)
#         return Service.objects.all()

def merchant_list(request):
    merchants = Merchant.objects.all()
    advert = PageAdvert.objects.filter(page_type='merchant', is_active=True).order_by('-updated_at').first()
    return render(request, 'merchants/merchant_list.html', {'merchants': merchants, 'advert': advert})

def category_detail(request, category_id):
    from django.utils import timezone
    from deals.models import Deal
    
    category = get_object_or_404(Category, id=category_id)
    
    # Check if this is a parent category with sub-categories
    subcategories = Category.objects.filter(parent=category, is_active=True)
    
    if subcategories.exists():
        # This is a parent category - show sub-categories page
        return render(request, 'category_subcategories.html', {
            'parent_category': category,
            'subcategories': subcategories,
        })
    
    # This is a leaf category - show merchants and deals
    merchants = Merchant.objects.filter(categories=category)
    
    # Filter for active deals only
    deals = Deal.objects.filter(
        category=category,
        status='active',
        start_datetime__lte=timezone.now(),
        end_datetime__gte=timezone.now()
    ).order_by('-created_at')
    
    from .models import PageAdvert
    advert = PageAdvert.objects.filter(page_type='category', category=category, is_active=True).order_by('-updated_at').first()
    
    return render(request, 'category_detail.html', {
        'category': category,
        'merchants': merchants,
        'deals': deals,
        'advert': advert
    })

def merchant_detail(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)
    return render(request, 'merchant_detail.html', {'merchant': merchant})
