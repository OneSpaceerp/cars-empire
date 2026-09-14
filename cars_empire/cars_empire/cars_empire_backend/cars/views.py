from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from users.models import User  # Import the custom user model
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import CarMake, CarModel
from .serializers import CarMakeSerializer, CarModelSerializer
from merchants.models import PageAdvert

# Create your views here.
def homepage(request):
    advert = PageAdvert.objects.filter(page_type='home', is_active=True).order_by('-updated_at').first()
    return render(request, 'index.html', {'advert': advert})
    
def cart_view(request):
    dummy_deal = {
        'title': 'Premium Car Wash',
        'merchant': {'name': 'Sparkle Clean'},
        'applicable_models': 'Sedans',
        'discount_price': '150.00'
    }

    context = {
        'cart_items': [{'deal': dummy_deal}],
        'cart_subtotal': '150.00',
        'cart_total': '150.00',
    }
    return render(request, 'cart.html', context)
    
def signup_view(request):
    """Render the signup page - registration is handled via JavaScript/API"""
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'signup.html')

def login_view(request):
    """Render the login page - authentication is handled via JavaScript/API"""
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')

class CarMakeListView(generics.ListCreateAPIView):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

class CarMakeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CarModelListView(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'make__name']
    ordering_fields = ['name', 'year_start', 'year_end']

    def get_queryset(self):
        queryset = CarModel.objects.all()
        make_id = self.request.query_params.get('make_id')
        if make_id:
            queryset = queryset.filter(make_id=make_id)
        return queryset

class CarModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CarModelSearchView(generics.ListAPIView):
    serializer_class = CarModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'make__name']
    ordering_fields = ['name', 'year_start', 'year_end']

    def get_queryset(self):
        queryset = CarModel.objects.all()
        make = self.request.query_params.get('make', None)
        if make is not None:
            queryset = queryset.filter(make__name=make)
        return queryset