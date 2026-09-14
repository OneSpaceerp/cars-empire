from django.urls import path
from . import views

urlpatterns = [
    # Car reviews
    path('cars/', views.CarReviewListView.as_view(), name='car-review-list'),
    path('cars/<int:pk>/', views.CarReviewDetailView.as_view(), name='car-review-detail'),
    
    # Merchant reviews
    path('merchants/', views.MerchantReviewListView.as_view(), name='merchant-review-list'),
    path('merchants/<int:pk>/', views.MerchantReviewDetailView.as_view(), name='merchant-review-detail'),
] 