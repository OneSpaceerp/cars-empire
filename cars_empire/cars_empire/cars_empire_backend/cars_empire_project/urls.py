from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Customize admin site
admin.site.site_header = "Cars Empire Administration"
admin.site.site_title = "Cars Empire Admin Portal"
admin.site.index_title = "Welcome to Cars Empire Admin Portal"

# Create schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Cars Empire API",
        default_version='v1',
        description="API documentation for Cars Empire",
        terms_of_service="https://carsempire.net/terms/",
        contact=openapi.Contact(email="contact@carsempire.net"),
        license=openapi.License(name="Proprietary License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URL patterns
api_patterns = [
    path('merchants/', include('merchants.api_urls')),
    path('deals/', include('deals.urls')),
    path('categories/', include('categories.urls')),
    path('cart/', include('cart.urls')),
    path('users/', include('users.urls')),
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.jwt')),
    path('cars/', include('cars.urls')),
    path('auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

def setup_db_view(request):
    import io, traceback
    out = io.StringIO()
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False, stdout=out, stderr=out)
        result = "SUCCESS: Database migrated successfully!\n\n" + out.getvalue()
        return HttpResponse(result, content_type='text/plain; charset=utf-8')
    except Exception:
        err = "ERROR: Migration failed:\n\n" + traceback.format_exc()
        return HttpResponse(err, content_type='text/plain; charset=utf-8', status=500)

urlpatterns = [
    path('setup-db/', setup_db_view, name='setup-db'),
    path('admin/', admin.site.urls),
    
    # Main website URLs
    path('', include('cars.urls')),
    path('deals/', include('deals.urls')),
    path('merchants/', include('merchants.urls')),
    path('coupons/', include('coupons.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
    
    # PWA URLs
    path('pwa/', include('pwa.urls')),
    
    # API URLs
    path('api/', include([
        path('users/', include('users.urls')),
        path('deals/', include('deals.api_urls')),
        path('merchants/', include('merchants.api_urls')),
        path('coupons/', include('coupons.urls')),
        path('cart/', include('cart.urls')),
        path('categories/', include('categories.urls')),
        path('reviews/', include('reviews.urls')),
        path('payments/', include('payments.urls')),
        path('cars/', include('cars.urls')),
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
    ])),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
