from django.shortcuts import render
from rest_framework import generics, filters, permissions
from .models import CarReview, MerchantReview
from .serializers import CarReviewSerializer, MerchantReviewSerializer

# Create your views here.

class ReviewMixin:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['rating', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CarReviewListView(ReviewMixin, generics.ListCreateAPIView):
    queryset = CarReview.objects.filter(is_public=True)
    serializer_class = CarReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_id = self.request.query_params.get('car', None)
        if car_id is not None:
            queryset = queryset.filter(car_id=car_id)
        return queryset

class CarReviewDetailView(ReviewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarReview.objects.filter(is_public=True)
    serializer_class = CarReviewSerializer

class MerchantReviewListView(ReviewMixin, generics.ListCreateAPIView):
    queryset = MerchantReview.objects.filter(is_public=True)
    serializer_class = MerchantReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        merchant_id = self.request.query_params.get('merchant', None)
        if merchant_id is not None:
            queryset = queryset.filter(merchant_id=merchant_id)
        return queryset

class MerchantReviewDetailView(ReviewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = MerchantReview.objects.filter(is_public=True)
    serializer_class = MerchantReviewSerializer
