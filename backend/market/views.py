from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.utils import timezone
from .models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket
from .serializers import (
    MarketMetricSerializer,
    AgentSerializer,
    NeighborhoodIntelSerializer,
    FastestGrowingMarketSerializer,
)
from articles.models import Article


@api_view(["GET"])
def market_metrics(request):
    metrics = MarketMetric.objects.all()
    return Response(MarketMetricSerializer(metrics, many=True).data)


@api_view(["GET"])
def top_agents(request):
    now = timezone.now()
    agents = Agent.objects.filter(period_year=now.year, period_month=now.month)
    if not agents.exists():
        agents = Agent.objects.all()
    return Response(AgentSerializer(agents, many=True).data)


@api_view(["GET"])
def neighborhood_intel(request):
    intel = NeighborhoodIntel.objects.all()
    return Response(NeighborhoodIntelSerializer(intel, many=True).data)


@api_view(["GET"])
def fastest_growing(request):
    markets = FastestGrowingMarket.objects.all()
    return Response(FastestGrowingMarketSerializer(markets, many=True).data)


# ── Template views ─────────────────────────────────────────────────────────────

def market_pulse_view(request):
    """
    Renders /market-pulse/ — Market Pulse category articles, plus the same
    market-metrics/top-agents sidebar widgets every other page shows.
    """
    articles = Article.objects.filter(
        category=Article.Category.MARKET_PULSE, status=Article.Status.PUBLISHED
    )
    market_metrics = MarketMetric.objects.all()[:5]
    top_agents_list = Agent.objects.order_by("rank")[:5]
    subscribed = request.session.pop("subscribed", False)

    context = {
        "market_metrics": market_metrics,
        "top_agents": top_agents_list,
        "articles": articles,
        "subscribed": subscribed,
    }
    return render(request, "market_pulse.html", context)


def agents_view(request):
    """
    Renders /agents/ — the full Top Agents leaderboard for the current
    month, plus Agent Watch category articles.

    Mirrors the top_agents API view's fallback: if no rows exist for the
    current period (e.g. a fresh dev DB, or data hasn't been refreshed
    yet this month), fall back to showing whatever rows exist rather
    than an empty page.
    """
    now = timezone.now()
    agents = Agent.objects.filter(period_year=now.year, period_month=now.month)
    if not agents.exists():
        agents = Agent.objects.all()

    watch_articles = Article.objects.filter(
        category=Article.Category.AGENT_WATCH, status=Article.Status.PUBLISHED
    )
    market_metrics = MarketMetric.objects.all()[:5]
    subscribed = request.session.pop("subscribed", False)

    context = {
        "market_metrics": market_metrics,
        "agents": agents,
        "watch_articles": watch_articles,
        "subscribed": subscribed,
    }
    return render(request, "agents.html", context)


def neighborhoods_view(request):
    """
    Renders /neighborhoods/ — the full Neighborhood Watch grid, plus
    Neighborhood Watch category articles.
    """
    neighborhoods = NeighborhoodIntel.objects.all()
    watch_articles = Article.objects.filter(
        category=Article.Category.NEIGHBORHOOD_WATCH, status=Article.Status.PUBLISHED
    )
    market_metrics = MarketMetric.objects.all()[:5]
    top_agents_list = Agent.objects.order_by("rank")[:5]
    subscribed = request.session.pop("subscribed", False)

    context = {
        "market_metrics": market_metrics,
        "top_agents": top_agents_list,
        "neighborhoods": neighborhoods,
        "watch_articles": watch_articles,
        "subscribed": subscribed,
    }
    return render(request, "neighborhoods.html", context)
