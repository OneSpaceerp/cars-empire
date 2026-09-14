# coupons/admin.py

from django.contrib import admin
from django.utils import timezone
from .models import Coupon, PromoCode, Redemption, CouponEvent, WorkOrder

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "coupon_code",
        "deal",
        "merchant",
        "user",
        "branch",
        "status",
        "valid_until",
        "redemption_datetime",
    )
    list_filter = (
        "status", 
        "merchant", 
        "branch", 
        "valid_until", 
        "created_at"
    )
    search_fields = (
        "coupon_code",
        "qr_token",
        "user__username",
        "user__email",
        "deal__title",
        "merchant__name",
    )
    readonly_fields = (
        "coupon_code",
        "qr_token",
        "code_hash",
        "purchase_datetime",
        "created_at",
        "updated_at",
    )
    actions = ["mark_as_available", "mark_as_expired", "mark_as_cancelled"]

    def mark_as_available(self, request, queryset):
        queryset.update(status="available")
        self.message_user(request, f"{queryset.count()} coupon(s) marked as Available.")
    mark_as_available.short_description = "Status -> Available"

    def mark_as_expired(self, request, queryset):
        queryset.update(status="expired")
        self.message_user(request, f"{queryset.count()} coupon(s) marked as Expired.")
    mark_as_expired.short_description = "Status -> Expired"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(request, f"{queryset.count()} coupon(s) marked as Cancelled.")
    mark_as_cancelled.short_description = "Status -> Cancelled"

@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "coupon",
        "merchant",
        "branch",
        "staff_user",
        "method",
        "status",
        "redeemed_at",
    )
    list_filter = (
        "status",
        "method",
        "merchant",
        "branch",
        "redeemed_at",
    )
    search_fields = (
        "receipt_number",
        "coupon__coupon_code",
        "merchant__name",
        "staff_user__username",
        "staff_user__email",
    )
    readonly_fields = ("receipt_number", "redeemed_at")

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "work_order_number",
        "coupon",
        "vehicle",
        "merchant",
        "branch",
        "technician",
        "status",
        "arrival_mileage_km",
        "started_at",
        "completed_at",
    )
    list_filter = (
        "status",
        "merchant",
        "branch",
        "created_at",
    )
    search_fields = (
        "work_order_number",
        "coupon__coupon_code",
        "vehicle__license_plate",
        "merchant__name",
        "technician__username",
    )
    readonly_fields = ("work_order_number", "created_at", "updated_at")

@admin.register(CouponEvent)
class CouponEventAdmin(admin.ModelAdmin):
    list_display = (
        "coupon",
        "event_type",
        "actor",
        "branch",
        "created_at",
    )
    list_filter = ("event_type", "created_at")
    search_fields = ("coupon__coupon_code", "actor__username")
    readonly_fields = ("coupon", "event_type", "actor", "branch", "notes", "metadata", "created_at")

    def has_add_permission(self, request):
        return False  # Immutable audit trail

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "min_purchase",
        "start_date",
        "end_date",
        "is_active",
        "times_used",
        "usage_limit",
    )
    list_filter = ("discount_type", "is_active", "start_date", "end_date")
    search_fields = ("code", "description")
