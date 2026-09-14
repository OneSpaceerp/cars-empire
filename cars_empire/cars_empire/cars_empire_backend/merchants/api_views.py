from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from math import radians, cos, sin, asin, sqrt
from .models import Merchant
from .serializers import MerchantSerializer

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'address_text']
    ordering_fields = ['name', 'created_at', 'rating']

    def get_queryset(self):
        queryset = Merchant.objects.all()
        verified_param = self.request.query_params.get('verified', None)
        if verified_param is not None and hasattr(Merchant, 'is_verified'):
            is_verified = verified_param.lower() in ['true', '1']
            queryset = queryset.filter(is_verified=is_verified)
        return queryset

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get merchants within a certain radius of a point"""
        try:
            lat = float(request.query_params.get('lat', 0))
            lng = float(request.query_params.get('lng', 0))
            radius = float(request.query_params.get('radius', 10))  # Default 10km radius
            
            # Get all merchants with valid coordinates
            merchants = Merchant.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )
            
            # Calculate distance for each merchant
            nearby_merchants = []
            for merchant in merchants:
                distance = self.calculate_distance(
                    lat, lng,
                    float(merchant.latitude),
                    float(merchant.longitude)
                )
                if distance <= radius:
                    merchant.distance = round(distance, 2)
                    nearby_merchants.append(merchant)
            
            # Sort by distance
            nearby_merchants.sort(key=lambda x: x.distance)
            
            serializer = self.get_serializer(nearby_merchants, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid coordinates or radius'}, status=400)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get merchants by category"""
        category_id = request.query_params.get('category_id')
        if category_id:
            merchants = Merchant.objects.filter(categories__id=category_id)
            serializer = self.get_serializer(merchants, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category ID is required'}, status=400) 