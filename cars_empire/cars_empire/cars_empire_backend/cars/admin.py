# cars/admin.py

from django.contrib import admin
from .models import CarMake, CarModel

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        "make",
        "name",
        "year_start",
        "year_end",
        "slug",
    )
    list_filter = ("make",)
    search_fields = (
        "name",
        "make__name",
    )
    prepopulated_fields = {"slug": ("make", "name")}
    # Adjust prepopulated_fields if needed based on how you want the slug generated

