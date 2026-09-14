from django.contrib import admin
from .models import InfoPage
from .models import ContactMessage

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'updated_at')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'slug', 'content')
    list_filter = ('is_active',)

admin.site.register(ContactMessage)
