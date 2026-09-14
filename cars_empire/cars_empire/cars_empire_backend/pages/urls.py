from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_us, name='contact_us'),  # Contact page first
    path('<slug:slug>/', views.info_page, name='info_page'),
] 