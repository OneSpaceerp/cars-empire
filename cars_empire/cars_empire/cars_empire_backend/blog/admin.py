# blog/admin.py

from django.contrib import admin
from .models import BlogCategory, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    
    class Meta:
        verbose_name = "Creators Category"
        verbose_name_plural = "Creators Categories"

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'is_featured', 'created_at', 'published_date')
    list_filter = ('is_published', 'is_featured', 'created_at', 'published_date')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    autocomplete_fields = ["author"]
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "author")
        }),
        ("Content", {
            "fields": ("content", "featured_image")
        }),
        ("Meta", {
            "fields": ("meta_description", "meta_keywords")
        }),
        ("Status", {
            "fields": ("is_published", "is_featured", "published_date")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )
    
    class Meta:
        verbose_name = "Creator Post"
        verbose_name_plural = "Creator Posts"

