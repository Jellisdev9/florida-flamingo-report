"""
articles/views.py

Contains both the existing DRF API views (kept as-is) and the new
Django template views added for server-rendered pages.

The template views follow a simple pattern:
  1. Query the database
  2. Build a context dictionary
  3. Call render(request, 'template.html', context) which fills the
     template's {{ variables }} with real data and returns an HttpResponse.
"""
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, get_object_or_404

from .models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer
from sales.models import NotableSale
from market.models import MarketMetric, NeighborhoodIntel, Agent


# ── DRF API views (unchanged) ─────────────────────────────────────────────────

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.filter(status=Article.Status.PUBLISHED)
    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status=Article.Status.PUBLISHED)
    serializer_class = ArticleDetailSerializer
    lookup_field = "slug"


@api_view(["GET"])
def featured_article(request):
    article = (
        Article.objects.filter(status=Article.Status.PUBLISHED, is_featured=True).first()
        or Article.objects.filter(status=Article.Status.PUBLISHED).first()
    )
    if not article:
        raise NotFound("No articles found.")
    return Response(ArticleDetailSerializer(article).data)


# ── Shared context helper ──────────────────────────────────────────────────────

def _base_context():
    """
    Returns the context variables that every page needs.

    base.html displays the market strip ticker and has a top agents sidebar
    available to all pages via partials. Rather than duplicating this query
    in every view, we call _base_context() and merge it in.

    The ** (double-star) operator unpacks a dict: {**_base_context(), 'key': val}
    creates a new dict with all keys from both sources.
    """
    return {
        # Powers the teal ticker bar in base.html — up to 5 tiles
        "market_metrics": MarketMetric.objects.all()[:5],
        # Powers the Top Agents partial sidebar
        "top_agents": Agent.objects.order_by("rank")[:5],
    }


# ── Template views ─────────────────────────────────────────────────────────────

def home_view(request):
    """
    Renders the homepage (/).

    Queries:
    - featured: the single article where is_featured=True (hero section)
    - articles: up to 5 non-featured published articles (card row)
    - closings: top 2 sales by price (Luxury Closings widget)
    - neighborhoods: up to 3 neighborhood intel cards

    The view also checks the session for a 'subscribed' flag — the subscribe
    view sets this after a successful POST so the homepage can show
    "You're subscribed!" instead of the email form.
    """
    featured = Article.objects.filter(
        is_featured=True, status=Article.Status.PUBLISHED
    ).first()

    # Exclude the featured article from the card row so it doesn't appear twice.
    # The conditional None handles the case where there's no featured article.
    articles = Article.objects.filter(status=Article.Status.PUBLISHED).exclude(
        pk=featured.pk if featured else None
    )[:5]

    closings = NotableSale.objects.filter(
        status=NotableSale.Status.PUBLISHED
    ).order_by("-price")[:2]
    neighborhoods = NeighborhoodIntel.objects.all()[:3]

    # session.pop() reads and deletes the flag in one call — prevents it
    # showing again if the user refreshes the page
    subscribed = request.session.pop("subscribed", False)

    context = {
        **_base_context(),
        "featured": featured,
        "articles": articles,
        "closings": closings,
        "neighborhoods": neighborhoods,
        "subscribed": subscribed,
    }
    return render(request, "home.html", context)


def article_detail_view(request, slug):
    """
    Renders an individual article page (/articles/<slug>/).

    get_object_or_404 queries Article by slug. If no match is found,
    Django automatically returns a 404 response — no if/else needed.

    'related' fetches up to 3 articles in the same category for the
    Related Stories sidebar widget.
    """
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)

    # Related stories: same category, not this article, up to 3
    related = Article.objects.filter(
        category=article.category,
        status=Article.Status.PUBLISHED,
    ).exclude(pk=article.pk)[:3]

    context = {
        **_base_context(),
        "article": article,
        "related": related,
    }
    return render(request, "article_detail.html", context)
