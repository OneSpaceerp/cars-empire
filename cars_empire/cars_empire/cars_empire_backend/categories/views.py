from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from merchants.models import Category
from merchants.serializers import CategorySerializer
import logging

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def all_for_carousel(self, request):
        """
        Get all categories for the carousel, including parent categories
        """
        try:
            # Get all active categories, prioritizing parent categories first
            parent_categories = Category.objects.filter(
                is_active=True, 
                parent__isnull=True
            ).order_by('name')
            
            child_categories = Category.objects.filter(
                is_active=True, 
                parent__isnull=False
            ).order_by('name')
            
            # Combine parent and child categories
            all_categories = list(parent_categories) + list(child_categories)
            
            logger.info(f"Carousel categories: {len(all_categories)} total (Parent: {parent_categories.count()}, Child: {child_categories.count()})")
            logger.info(f"Category names: {[cat.name for cat in all_categories]}")
            
            serializer = self.get_serializer(all_categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in all_for_carousel: {e}")
            return Response({'error': str(e)}, status=500) 