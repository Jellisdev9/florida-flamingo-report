"""
backend/sitemaps.py

Sitemap classes for django.contrib.sitemaps. Spans multiple apps
(articles, sales, plus the static category/utility pages), so it lives
alongside urls.py rather than inside a single app — same reasoning as
urls.py itself coordinating routes across apps.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from articles.models import Article
from sales.models import NotableSale


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(status=Article.Status.PUBLISHED)

    def location(self, obj):
        return reverse("article_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.published_date


class NotableSaleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return NotableSale.objects.filter(status=NotableSale.Status.PUBLISHED)

    def location(self, obj):
        return reverse("sale_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.close_date


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [
            "home",
            "article_archive",
            "notable_sales",
            "market_pulse",
            "agents",
            "neighborhoods",
            "about",
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    "articles": ArticleSitemap,
    "sales": NotableSaleSitemap,
    "pages": StaticViewSitemap,
}
