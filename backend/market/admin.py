from django.contrib import admin
from .models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket


@admin.register(MarketMetric)
class MarketMetricAdmin(admin.ModelAdmin):
    list_display = ["city", "metric_label", "value_display", "change_display", "is_positive", "sort_order", "source_name"]
    list_editable = ["sort_order", "is_positive"]
    search_fields = ["city", "metric_label", "source_name"]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["rank", "name", "location", "volume_display", "period_month", "period_year", "source_name"]
    list_display_links = ["name"]
    list_editable = ["rank"]
    search_fields = ["name", "location", "source_name"]


@admin.register(NeighborhoodIntel)
class NeighborhoodIntelAdmin(admin.ModelAdmin):
    list_display = ["neighborhood", "city", "tag", "sort_order", "source_name"]
    list_editable = ["sort_order"]
    search_fields = ["neighborhood", "city", "source_name"]


@admin.register(FastestGrowingMarket)
class FastestGrowingMarketAdmin(admin.ModelAdmin):
    list_display = ["rank", "location", "change_display", "source_name"]
    list_display_links = ["location"]
    list_editable = ["rank"]
    search_fields = ["location", "source_name"]
