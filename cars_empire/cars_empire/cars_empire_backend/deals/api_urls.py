from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'', views.DealViewSet, basename='deal')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'alerts', views.DealAlertViewSet, basename='deal-alert')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

# API URLs
urlpatterns = [
    path('', include(router.urls)),
]
