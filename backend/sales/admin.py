from django.contrib import admin
from .models import NotableSale


@admin.register(NotableSale)
class NotableSaleAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "city", "region", "property_type", "close_date", "is_featured"]
    list_filter = ["region", "property_type", "is_featured"]
    list_editable = ["is_featured"]
    search_fields = ["title", "city", "location"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "close_date"
