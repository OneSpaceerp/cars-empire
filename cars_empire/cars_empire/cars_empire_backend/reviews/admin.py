# reviews/admin.py

from django.contrib import admin
from .models import CarReview, MerchantReview  # Temporarily remove ServiceReview

class BaseReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'rating', 'created_at', 'is_verified', 'is_public')
    list_filter = ('rating', 'is_verified', 'is_public', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(CarReview)
class CarReviewAdmin(BaseReviewAdmin):
    list_display = BaseReviewAdmin.list_display + ('car',)
    list_filter = BaseReviewAdmin.list_filter + ('car__make',)

@admin.register(MerchantReview)
class MerchantReviewAdmin(BaseReviewAdmin):
    list_display = BaseReviewAdmin.list_display + ('merchant',)

# Temporarily comment out ServiceReview admin
# @admin.register(ServiceReview)
# class ServiceReviewAdmin(BaseReviewAdmin):
#     list_display = BaseReviewAdmin.list_display + ('service',)

