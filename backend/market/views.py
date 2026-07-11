from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket
from .serializers import (
    MarketMetricSerializer,
    AgentSerializer,
    NeighborhoodIntelSerializer,
    FastestGrowingMarketSerializer,
)


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
