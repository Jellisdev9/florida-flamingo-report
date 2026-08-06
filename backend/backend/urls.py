"""
Root URL configuration for the Florida Flamingo Report backend.

URL routing works like a switch statement — Django checks each path() in
order and calls the view function for the first match.

We keep all existing /api/ routes intact (the DRF API is still useful for
mobile/RSS/future use) and add the new template-rendered page URLs below them.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Import the template views — these render HTML pages
from articles.views import home_view, article_detail_view
from sales.views import notable_sales_view
from subscribers.views import subscribe_view


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    # ── Django admin ──────────────────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ── Health check ──────────────────────────────────────────────────────────
    path("api/healthz/", health_check),

    # ── DRF API routes (kept — costs nothing, useful for mobile/RSS later) ───
    # include() pulls in the urlpatterns list from each app's urls.py
    path("api/", include("articles.urls")),
    path("api/", include("sales.urls")),
    path("api/", include("market.urls")),
    path("api/", include("subscribers.urls")),

    # ── Template-rendered pages ───────────────────────────────────────────────
    # The name= argument lets views/templates use reverse('home') or
    # {% url 'home' %} instead of hardcoding the URL string.

    # Homepage — "" matches the root path "/"
    path("", home_view, name="home"),

    # Individual article page — <slug:slug> captures URL-safe strings like
    # "naples-bayfront-estate" and passes them as the 'slug' keyword argument
    path("articles/<slug:slug>/", article_detail_view, name="article_detail"),

    # Notable sales grid
    path("notable-sales/", notable_sales_view, name="notable_sales"),

    # Newsletter subscribe — POST only (the view enforces this with @require_POST)
    path("subscribe/", subscribe_view, name="subscribe"),
]
