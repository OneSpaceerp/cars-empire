# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserCar

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_select_related = ("profile",)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Register the custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)

@admin.register(UserCar)
class UserCarAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "car_model",
        "year",
        "vin",
        "registration_plate",
    )
    list_filter = (
        "user",
        "car_model__make",
        "year",
    )
    search_fields = (
        "user__username",
        "car_model__name",
        "car_model__make__name",
        "vin",
        "registration_plate",
    )
    autocomplete_fields = ["user", "car_model"]

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "make",
        "model",
        "year",
        "license_plate",
        "fuel_type",
        "is_primary",
    )
    list_filter = (
        "make",
        "fuel_type",
        "is_primary",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "make__name",
        "model__name",
        "license_plate",
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('deal', 'vehicle', 'branch', 'quantity', 'price', 'discount_amount', 'line_total')
    readonly_fields = ('line_total',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "total",
        "currency",
        "created_at",
    )
    list_filter = (
        "status",
        "currency",
        "created_at",
    )
    search_fields = (
        "order_number",
        "user__username",
        "user__email",
        "user__phone",
    )
    readonly_fields = ("order_number", "created_at", "updated_at")
    inlines = [OrderItemInline]
    actions = ["mark_as_paid_and_issue_coupons"]

    def mark_as_paid_and_issue_coupons(self, request, queryset):
        from coupons.models import generate_unique_coupons_for_order
        issued_count = 0
        for order in queryset:
            if order.status != 'paid':
                order.status = 'paid'
                order.save()
            coupons = generate_unique_coupons_for_order(order)
            issued_count += len(coupons)
        self.message_user(request, f"Selected orders processed. {issued_count} unique service coupons minted successfully.")
    mark_as_paid_and_issue_coupons.short_description = "Mark as Paid & Generate Unique Coupons"


