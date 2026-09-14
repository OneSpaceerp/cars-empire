from django.urls import path
from . import views
from .views import merchant_list, category_detail, merchant_detail

urlpatterns = [
    path('', views.merchant_list, name='merchant_list'),  # HTML page for /merchants/
    path('nearby/', views.NearbyMerchantsView.as_view(), name='merchant-nearby'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('<int:merchant_id>/', merchant_detail, name='merchant_detail'),  # Merchant detail page
] 