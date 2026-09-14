# deals/admin.py

from django.contrib import admin
from .models import Deal, DealImage

class DealImageInline(admin.TabularInline):
    model = DealImage
    extra = 1
    fields = ("image", "alt_text")

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "merchant",
        "category",
        "original_price",
        "discount_price",
        "start_datetime",
        "end_datetime",
        "status",
        "is_active",
        "is_featured"
    )
    list_filter = (
        "status",
        "merchant",
        "category",
        "start_datetime",
        "end_datetime",
        "is_featured"
    )
    search_fields = (
        "title",
        "description",
        "merchant__name",
        "category__name",
    )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["merchant", "category", "applicable_models"]
    inlines = [DealImageInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "merchant", "category")}),
        (
            "Pricing & Validity",
            {
                "fields": (
                    "original_price",
                    "discount_price",
                    "start_datetime",
                    "end_datetime",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "description",
                    "terms_and_conditions",
                    "redemption_instructions",
                    "applicable_models",
                )
            },
        ),
        (
            "Status & Visibility",
            {"fields": ("status", "quantity_limit", "is_featured")},
        ),
    )

@admin.register(DealImage)
class DealImageAdmin(admin.ModelAdmin):
    list_display = ("deal", "image", "alt_text")
    search_fields = ("deal__title", "alt_text")
    autocomplete_fields = ["deal"]

