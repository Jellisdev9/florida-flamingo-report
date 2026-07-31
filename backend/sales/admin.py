from django.contrib import admin
from .models import NotableSale


@admin.register(NotableSale)
class NotableSaleAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "city", "region", "property_type", "close_date", "is_featured", "status", "source_name"]
    list_filter = ["region", "property_type", "is_featured", "status"]
    list_editable = ["is_featured", "status"]
    search_fields = ["title", "city", "location", "source_name"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "close_date"
