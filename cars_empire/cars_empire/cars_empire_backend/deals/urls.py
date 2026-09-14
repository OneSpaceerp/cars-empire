from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'deals', views.DealViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'alerts', views.DealAlertViewSet, basename='deal-alert')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

# Frontend URLs
urlpatterns = [
    path('page/', views.deals_page, name='deals'),
    path('<slug:slug>/', views.deal_detail, name='deal-detail'),
]

# API URLs
api_urlpatterns = [
    path('', include(router.urls)),
] 