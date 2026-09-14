# merchants/admin.py

from django.contrib import admin
from .models import Category, Merchant, Branch, MerchantUser, MerchantImage, PageAdvert, PageAdvertImage, PageAdvertVideo, Service
from cars.models import CarMake

class MerchantImageInline(admin.TabularInline):
    model = MerchantImage
    extra = 1
    fields = ('image', 'caption', 'image_type', 'is_primary', 'order')
    show_change_link = True

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1
    fields = ("name", "address_text", "contact_phone")

class MerchantUserInline(admin.TabularInline):
    model = MerchantUser
    extra = 1
    fields = ("user", "role")
    autocomplete_fields = ["user"]

class PageAdvertImageInline(admin.TabularInline):
    model = PageAdvertImage
    extra = 1

class PageAdvertVideoInline(admin.TabularInline):
    model = PageAdvertVideo
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'parent', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at', 'parent')
    fields = ('name', 'parent', 'slug', 'description', 'icon', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_verified', 'is_featured', 'display_order', 'created_at')
    list_editable = ('display_order',)
    list_filter = ('is_verified', 'is_featured', 'created_at', 'categories')
    search_fields = ('name', 'email', 'phone_number', 'address_text')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('categories', 'makes',)
    inlines = [MerchantImageInline, BranchInline, MerchantUserInline]  # Add MerchantImageInline
    actions = ["verify_merchants", "feature_merchants"]

    fieldsets = (
        ("Basic Info", {
            'fields': (
                'name', 'phone_number', 'email', 'website', 'categories', 'makes',
                'logo', 'description', 'address_text', 'latitude', 'longitude',
            ),
            'description': 'Assign makes to specify which car makes this merchant services. Leave blank to indicate all makes.'
        }),
        ("Social Media", {
            'fields': (
                'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'tiktok_url', 'youtube_url',
            ),
            'classes': ('collapse',)
        }),
        ("Business Info", {
            'fields': (
                'rating', 'is_verified', 'is_featured',
            ),
            'classes': ('collapse',)
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def verify_merchants(self, request, queryset):
        queryset.update(is_verified=True)
    verify_merchants.short_description = "Verify selected merchants"

    def feature_merchants(self, request, queryset):
        queryset.update(is_featured=True)
    feature_merchants.short_description = "Feature selected merchants"

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'contact_phone', 'address_text', 'is_main')
    list_filter = ('merchant', 'is_main')
    search_fields = ('name', 'address_text', 'contact_phone')
    autocomplete_fields = ["merchant"]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'branch', 'category', 'price', 'duration', 'is_available')
    list_filter = ('merchant', 'is_available', 'branch', 'category')
    search_fields = ('name', 'description', 'merchant__name')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('name', 'merchant', 'branch', 'category', 'description', 'price', 'duration', 'is_available', 'created_at', 'updated_at')

@admin.register(MerchantImage)
class MerchantImageAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'image_type', 'caption', 'is_primary', 'order', 'created_at')
    list_filter = ('image_type', 'is_primary', 'created_at')
    search_fields = ('merchant__name', 'caption')
    list_editable = ('order', 'is_primary')
    autocomplete_fields = ['merchant']

@admin.register(MerchantUser)
class MerchantUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'merchant', 'role', 'is_active')
    list_filter = ('merchant', 'role', 'is_active')
    search_fields = ('user__username', 'merchant__name')
    autocomplete_fields = ["user", "merchant"]

@admin.register(PageAdvert)
class PageAdvertAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'category', 'merchant', 'is_active', 'created_at')
    list_filter = ('page_type', 'is_active', 'created_at')
    search_fields = ('title',)
    inlines = [PageAdvertImageInline, PageAdvertVideoInline]
    autocomplete_fields = ['category', 'merchant']
    fieldsets = (
        (None, {
            'fields': ('title', 'page_type', 'category', 'merchant', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PageAdvertImage)
class PageAdvertImageAdmin(admin.ModelAdmin):
    list_display = ('advert', 'order')
    search_fields = ('advert__title',)
    autocomplete_fields = ['advert']

@admin.register(PageAdvertVideo)
class PageAdvertVideoAdmin(admin.ModelAdmin):
    list_display = ('advert', 'order')
    search_fields = ('advert__title',)
    autocomplete_fields = ['advert']

