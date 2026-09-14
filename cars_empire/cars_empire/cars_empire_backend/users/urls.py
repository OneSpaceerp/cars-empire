from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from . import views
from .views import VehicleViewSet, UserOrderListView, UserCouponListView, UserCouponDetailView, ChangePasswordView

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')

urlpatterns = [
    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('set_password/', ChangePasswordView.as_view(), name='set_password'),
    path('orders/', UserOrderListView.as_view(), name='user-orders'),
    path('coupons/', UserCouponListView.as_view(), name='user-coupons'),
    path('coupons/<int:pk>/', UserCouponDetailView.as_view(), name='user-coupon-detail'),
    path('', include(router.urls)),
] 