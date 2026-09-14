from django.urls import path
from . import views

app_name = 'pwa'

urlpatterns = [
    # Test URL
    path('test/', views.pwa_test, name='test'),
    path('api-test/', views.pwa_api_test, name='api_test'),
    
    # Main PWA pages
    path('', views.pwa_home, name='home'),
    path('deals/', views.pwa_deals, name='deals'),
    path('merchants/', views.pwa_merchants, name='merchants'),
    path('cart/', views.pwa_cart, name='cart'),
    path('checkout/', views.pwa_checkout, name='checkout'),
    path('profile/', views.pwa_profile, name='profile'),
    path('login/', views.pwa_login, name='login'),
    path('register/', views.pwa_register, name='register'),
    path('search/', views.pwa_search, name='search'),
    
    # Detail pages
    path('merchant/<int:merchant_id>/', views.pwa_merchant_detail, name='merchant_detail'),
    path('deal/<int:deal_id>/', views.pwa_deal_detail, name='deal_detail'),
    path('category/<int:category_id>/', views.pwa_category_detail, name='category_detail'),
    
    # API endpoints
    path('api/advert/', views.pwa_advert_api, name='advert_api'),
    path('api/contact/', views.pwa_contact_api, name='contact_api'),
    path('api/translations/', views.pwa_translations_api, name='translations_api'),
] 