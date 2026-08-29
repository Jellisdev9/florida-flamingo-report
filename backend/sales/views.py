"""
sales/views.py

DRF API views (kept) + Django template view for the Notable Sales page.
"""
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import NotableSale
from .serializers import NotableSaleSerializer, NotableSaleListSerializer
from market.models import MarketMetric, FastestGrowingMarket, Agent


# ── DRF API views (unchanged) ─────────────────────────────────────────────────

class NotableSaleListView(generics.ListAPIView):
    queryset = NotableSale.objects.filter(status=NotableSale.Status.PUBLISHED)
    serializer_class = NotableSaleListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["region", "property_type"]


@api_view(["GET"])
def featured_sale(request):
    sale = NotableSale.objects.filter(
        is_featured=True, status=NotableSale.Status.PUBLISHED
    ).first()
    if not sale:
        raise NotFound("No featured sale found.")
    return Response(NotableSaleSerializer(sale).data)


@api_view(["GET"])
def top_closings(request):
    sales = NotableSale.objects.filter(status=NotableSale.Status.PUBLISHED).order_by("-price")[:5]
    return Response(NotableSaleListSerializer(sales, many=True).data)


# ── Template view ──────────────────────────────────────────────────────────────

# Maps the URL query param value to its human-readable label.
# e.g. ?region=TAMPA_BAY → "Tampa Bay" in the filter tab.
# This dict is passed to the template so it can render the tab buttons
# without hardcoding any region names in the HTML.
REGION_MAP = {
    "SOUTH_FLORIDA": "South Florida",
    "TAMPA_BAY": "Tampa Bay",
    "ORLANDO": "Orlando",
    "JACKSONVILLE": "Jacksonville",
    "PANHANDLE": "Panhandle",
}


def notable_sales_view(request):
    """
    Renders /notable-sales/.

    Region filtering uses a simple query string: ?region=SOUTH_FLORIDA.
    The page reloads when the user clicks a region tab — no JavaScript needed.

    Context variables:
    - featured:        the is_featured=True sale (hero card)
    - sales:           filtered (or all) sales for the grid
    - top_closings:    top 5 by price for the sidebar widget
    - fastest_growing: fastest growing markets for the sidebar widget
    - active_region:   the currently selected region code (or '' for All)
    - region_map:      REGION_MAP dict so the template can build tab links
    - subscribed:      True if the user just subscribed (session flag)
    """
    # request.GET is a dict of URL query parameters
    # e.g. for ?region=ORLANDO, request.GET.get('region') returns 'ORLANDO'
    region = request.GET.get("region")

    featured = NotableSale.objects.filter(
        is_featured=True, status=NotableSale.Status.PUBLISHED
    ).first()

    sales = NotableSale.objects.filter(status=NotableSale.Status.PUBLISHED)
    # Only apply the filter if the region code is a known valid value
    if region and region in REGION_MAP:
        sales = sales.filter(region=region)
    sales = sales[:20]

    top_closings = NotableSale.objects.filter(
        status=NotableSale.Status.PUBLISHED
    ).order_by("-price")[:5]

    # Same current-period-with-fallback pattern as agents_view (market/views.py):
    # without it, refreshing this data periodically would just accumulate rows
    # forever with no natural "current" set to display.
    now = timezone.now()
    fastest_growing = FastestGrowingMarket.objects.filter(
        period_year=now.year, period_month=now.month
    ).order_by("rank")[:5]
    if not fastest_growing.exists():
        fastest_growing = FastestGrowingMarket.objects.order_by("rank")[:5]

    market_metrics = MarketMetric.objects.all()[:5]
    top_agents = Agent.objects.order_by("rank")[:5]

    subscribed = request.session.pop("subscribed", False)

    context = {
        "market_metrics": market_metrics,
        "top_agents": top_agents,
        "featured": featured,
        "sales": sales,
        "top_closings": top_closings,
        "fastest_growing": fastest_growing,
        # active_region is '' when no filter — the template checks `if not active_region`
        "active_region": region or "",
        "subscribed": subscribed,
        "region_map": REGION_MAP,
    }
    return render(request, "notable_sales.html", context)


def sale_detail_view(request, slug):
    """
    Renders /notable-sales/<slug>/ — an individual sale's detail page.

    Previously didn't exist at all: NotableSale.slug was defined on the
    model but nothing routed to it, so grid cards, the featured-sale
    hero, and the Top Closings sidebar were all dead ends. sale.article
    is optional (most sales have no full editorial write-up — only 1 of
    8 in the fixture data does), so the template shows a link to it
    only when set.
    """
    sale = get_object_or_404(NotableSale, slug=slug, status=NotableSale.Status.PUBLISHED)

    market_metrics = MarketMetric.objects.all()[:5]
    top_agents = Agent.objects.order_by("rank")[:5]
    subscribed = request.session.pop("subscribed", False)

    context = {
        "market_metrics": market_metrics,
        "top_agents": top_agents,
        "sale": sale,
        "subscribed": subscribed,
        # Social-sharing meta tags (base.html) — real content instead of
        # the sitewide default.
        "page_title": sale.title,
        "meta_description": f"{sale.title} — {sale.price_display} in {sale.city}, FL.",
        "og_image": sale.hero_image_url or None,
    }
    return render(request, "notable_sale_detail.html", context)
