from django.urls import path
from . import views

urlpatterns = [
    path('', views.CouponListView.as_view(), name='coupon-list'),
    path('<int:pk>/', views.CouponDetailView.as_view(), name='coupon-detail'),
    
    # Section 17 Merchant Redemption Engine Endpoints
    path('merchant/validate/', views.MerchantCouponValidateView.as_view(), name='merchant-coupon-validate'),
    path('merchant/redeem/', views.MerchantCouponRedeemView.as_view(), name='merchant-coupon-redeem'),
    path('merchant/recent-redemptions/', views.MerchantRecentRedemptionsView.as_view(), name='merchant-recent-redemptions'),
    
    # Checkout Promo Codes
    path('promos/validate/', views.PromoCodeValidateView.as_view(), name='promo-validate'),
    
    # Backward compatibility routes
    path('validate/', views.MerchantCouponValidateView.as_view(), name='coupon-validate-compat'),
    path('redeem/', views.MerchantCouponRedeemView.as_view(), name='coupon-redeem-compat'),
    path('redeem-qr/', views.MerchantCouponRedeemView.as_view(), name='coupon-redeem-qr-compat'),
    path('recent-redemptions/', views.MerchantRecentRedemptionsView.as_view(), name='coupon-recent-redemptions-compat'),
] 