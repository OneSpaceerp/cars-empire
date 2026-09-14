from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import logging

from merchants.models import Merchant, Category, PageAdvert
from deals.models import Deal
from users.models import User
from merchants.serializers import PageAdvertSerializer

logger = logging.getLogger(__name__)

def pwa_test(request):
    """Simple test view to check if PWA is working"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    from django.utils import timezone
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
        'server_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
    }
    
    return render(request, 'pwa/test.html', context)

def pwa_home(request):
    """PWA Homepage view"""
    # Get language from request or default to English
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    # Get featured deals - use status='active' instead of is_active
    featured_deals = Deal.objects.filter(is_featured=True, status='active')[:6]
    
    # Get categories for carousel
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    # Get home page advert
    try:
        advert = PageAdvert.objects.filter(page_type='home', is_active=True).first()
    except Exception as e:
        logger.warning(f"Error loading home advert: {e}")
        advert = None
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
        'featured_deals': featured_deals,
        'categories': categories,
        'advert': advert,
    }
    
    return render(request, 'pwa/index.html', context)

def pwa_deals(request):
    """PWA Deals page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    # Get deals with pagination - use status='active' instead of is_active
    page = request.GET.get('page', 1)
    category_id = request.GET.get('category')
    merchant_id = request.GET.get('merchant')
    
    deals = Deal.objects.filter(status='active')
    
    if category_id:
        deals = deals.filter(category_id=category_id)
    
    if merchant_id:
        deals = deals.filter(merchant_id=merchant_id)
    
    # Get categories for filter
    categories = Category.objects.filter(is_active=True)
    
    # Get page advert
    try:
        advert = PageAdvert.objects.filter(page_type='deals', is_active=True).first()
    except Exception as e:
        logger.warning(f"Error loading deals advert: {e}")
        advert = None
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
        'deals': deals,
        'categories': categories,
        'advert': advert,
    }
    
    return render(request, 'pwa/deals.html', context)

def pwa_merchants(request):
    """PWA Merchants page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    # Get merchants
    merchants = Merchant.objects.filter(is_active=True).order_by('display_order', 'name')
    
    # Get categories for filter
    categories = Category.objects.filter(is_active=True)
    
    # Get page advert
    try:
        advert = PageAdvert.objects.filter(page_type='merchant', is_active=True).first()
    except Exception as e:
        logger.warning(f"Error loading merchants advert: {e}")
        advert = None
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
        'merchants': merchants,
        'categories': categories,
        'advert': advert,
    }
    
    return render(request, 'pwa/merchants.html', context)

def pwa_merchant_detail(request, merchant_id):
    """PWA Merchant detail view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    try:
        merchant = Merchant.objects.get(id=merchant_id, is_active=True)
        
        # Get merchant deals - use status='active' instead of is_active
        deals = Deal.objects.filter(merchant=merchant, status='active')
        
        context = {
            'current_language': language,
            'text_direction': 'rtl' if language == 'ar' else 'ltr',
            'merchant': merchant,
            'deals': deals,
        }
        
        return render(request, 'pwa/merchant_detail.html', context)
    except Merchant.DoesNotExist:
        return JsonResponse({'error': 'Merchant not found'}, status=404)

def pwa_deal_detail(request, deal_id):
    """PWA Deal detail view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    try:
        # Get deal - use status='active' instead of is_active
        deal = Deal.objects.get(id=deal_id, status='active')
        
        context = {
            'current_language': language,
            'text_direction': 'rtl' if language == 'ar' else 'ltr',
            'deal': deal,
        }
        
        return render(request, 'pwa/deal_detail.html', context)
    except Deal.DoesNotExist:
        return JsonResponse({'error': 'Deal not found'}, status=404)

def pwa_category_detail(request, category_id):
    """PWA Category detail view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    try:
        category = Category.objects.get(id=category_id, is_active=True)
        
        # Get deals for this category - use status='active' instead of is_active
        deals = Deal.objects.filter(category=category, status='active')
        
        # Get subcategories
        subcategories = Category.objects.filter(parent=category, is_active=True)
        
        context = {
            'current_language': language,
            'text_direction': 'rtl' if language == 'ar' else 'ltr',
            'category': category,
            'deals': deals,
            'subcategories': subcategories,
        }
        
        return render(request, 'pwa/category_detail.html', context)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

def pwa_cart(request):
    """PWA Cart page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
    }
    
    return render(request, 'pwa/cart.html', context)

def pwa_checkout(request):
    """PWA Checkout page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
    }
    
    return render(request, 'pwa/checkout.html', context)

def pwa_profile(request):
    """PWA Profile page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
    }
    
    return render(request, 'pwa/profile.html', context)

def pwa_login(request):
    """PWA Login page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
    }
    
    return render(request, 'pwa/login.html', context)

def pwa_register(request):
    """PWA Register page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
    }
    
    return render(request, 'pwa/register.html', context)

def pwa_search(request):
    """PWA Search page view"""
    language = request.GET.get('lang', 'en')
    request.session['language'] = language
    
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    results = {
        'deals': [],
        'merchants': [],
        'categories': []
    }
    
    if query:
        if search_type in ['all', 'deals']:
            results['deals'] = Deal.objects.filter(
                title__icontains=query,
                status='active'
            )[:10]
        
        if search_type in ['all', 'merchants']:
            results['merchants'] = Merchant.objects.filter(
                name__icontains=query,
                is_active=True
            )[:10]
        
        if search_type in ['all', 'categories']:
            results['categories'] = Category.objects.filter(
                name__icontains=query,
                is_active=True
            )[:10]
    
    context = {
        'current_language': language,
        'text_direction': 'rtl' if language == 'ar' else 'ltr',
        'query': query,
        'search_type': search_type,
        'results': results,
    }
    
    return render(request, 'pwa/search.html', context)

# API Views for PWA
@api_view(['GET'])
def pwa_advert_api(request):
    """API endpoint for getting page adverts"""
    page = request.GET.get('page', 'home')
    
    try:
        advert = PageAdvert.objects.filter(page_type=page, is_active=True).first()
        if advert:
            serializer = PageAdvertSerializer(advert, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'message': 'No advert found'}, status=404)
    except Exception as e:
        logger.error(f'Error getting advert for page {page}: {e}')
        return Response({'error': 'Internal server error'}, status=500)

@api_view(['POST'])
@csrf_exempt
def pwa_contact_api(request):
    """API endpoint for contact form submission"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'error': f'{field} is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Here you would typically save to database
        # For now, just log the contact
        logger.info(f'Contact form submission: {data}')
        
        return Response({'message': 'Message sent successfully'})
        
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f'Error processing contact form: {e}')
        return Response(
            {'error': 'Internal server error'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def pwa_translations_api(request):
    """API endpoint for getting translations"""
    language = request.GET.get('lang', 'en')
    
    try:
        # Load translation file
        import os
        from django.conf import settings
        
        translation_file = os.path.join(
            settings.STATIC_ROOT, 
            'pwa', 
            'translations', 
            f'{language}.json'
        )
        
        if os.path.exists(translation_file):
            with open(translation_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
            return Response(translations)
        else:
            return Response({'error': 'Translation not found'}, status=404)
            
    except Exception as e:
        logger.error(f'Error loading translations for {language}: {e}')
        return Response({'error': 'Internal server error'}, status=500)

@api_view(['GET'])
def pwa_api_test(request):
    """API test endpoint to check if APIs are working"""
    try:
        # Test basic API functionality
        from merchants.models import Category, Merchant
        from deals.models import Deal
        from django.utils import timezone
        
        category_count = Category.objects.filter(is_active=True).count()
        merchant_count = Merchant.objects.filter(is_active=True).count()
        deal_count = Deal.objects.filter(status='active').count()
        
        return Response({
            'status': 'success',
            'message': 'PWA APIs are working correctly',
            'data': {
                'categories': category_count,
                'merchants': merchant_count,
                'deals': deal_count,
                'timestamp': timezone.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f'API test error: {e}')
        return Response({
            'status': 'error',
            'message': f'API test failed: {str(e)}'
        }, status=500)

# Utility functions
def get_user_location(request):
    """Get user location from request headers or session"""
    # This would typically get location from request headers
    # For now, return default coordinates
    return {
        'latitude': 25.2048,  # Default to Riyadh
        'longitude': 55.2708,
    }

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    import math
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c 