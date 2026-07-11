from rest_framework import serializers
from .models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket


class MarketMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMetric
        fields = ["city", "metric_label", "value_display", "change_display", "is_positive"]


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["rank", "name", "location", "volume_display"]


class NeighborhoodIntelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeighborhoodIntel
        fields = ["neighborhood", "city", "description", "tag"]


class FastestGrowingMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastestGrowingMarket
        fields = ["rank", "location", "change_display"]
