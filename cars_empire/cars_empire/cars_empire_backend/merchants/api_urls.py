from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MerchantViewSet, BranchViewSet, MerchantUserViewSet
from coupons.views import (
    MerchantCouponRedeemView, 
    MerchantRecentRedemptionsView, 
    MerchantCouponValidateView
)

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'users', MerchantUserViewSet, basename='merchant-user')
router.register(r'', MerchantViewSet, basename='merchant')

urlpatterns = [
    # Direct merchant portal compatibility routes
    path('redeem-qr/', MerchantCouponRedeemView.as_view(), name='merchant-redeem-qr'),
    path('recent-redemptions/', MerchantRecentRedemptionsView.as_view(), name='merchant-recent-redemptions'),
    path('validate-coupon/', MerchantCouponValidateView.as_view(), name='merchant-validate-coupon'),
] + router.urls 