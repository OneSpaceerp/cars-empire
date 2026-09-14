from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('cart/', views.cart_view, name='cart'),
    path('makes/', views.CarMakeListView.as_view(), name='make-list'),
    path('makes/<int:pk>/', views.CarMakeDetailView.as_view(), name='make-detail'),
    path('models/', views.CarModelListView.as_view(), name='model-list'),
    path('models/<int:pk>/', views.CarModelDetailView.as_view(), name='model-detail'),
    path('models/search/', views.CarModelSearchView.as_view(), name='model-search'),
] 