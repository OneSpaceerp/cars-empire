from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarMakeListView.as_view(), name='api-cars-root'),
    path('makes/', views.CarMakeListView.as_view(), name='api-make-list'),
    path('makes/<int:pk>/', views.CarMakeDetailView.as_view(), name='api-make-detail'),
    path('models/', views.CarModelListView.as_view(), name='api-model-list'),
    path('models/<int:pk>/', views.CarModelDetailView.as_view(), name='api-model-detail'),
    path('models/search/', views.CarModelSearchView.as_view(), name='api-model-search'),
]
