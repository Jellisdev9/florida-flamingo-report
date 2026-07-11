from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["headline", "category", "published_date", "is_featured", "is_published"]
    list_filter = ["category", "is_featured", "is_published"]
    list_editable = ["is_featured", "is_published"]
    search_fields = ["headline", "byline"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
