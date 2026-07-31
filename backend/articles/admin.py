from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["headline", "category", "published_date", "is_featured", "status", "source_name"]
    list_filter = ["category", "is_featured", "status"]
    list_editable = ["is_featured", "status"]
    search_fields = ["headline", "byline", "source_name"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
