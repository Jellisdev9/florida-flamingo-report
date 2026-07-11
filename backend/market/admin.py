from django.contrib import admin
from .models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket


@admin.register(MarketMetric)
class MarketMetricAdmin(admin.ModelAdmin):
    list_display = ["city", "metric_label", "value_display", "change_display", "is_positive", "sort_order"]
    list_editable = ["sort_order", "is_positive"]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["rank", "name", "location", "volume_display", "period_month", "period_year"]
    list_display_links = ["name"]
    list_editable = ["rank"]


@admin.register(NeighborhoodIntel)
class NeighborhoodIntelAdmin(admin.ModelAdmin):
    list_display = ["neighborhood", "city", "tag", "sort_order"]
    list_editable = ["sort_order"]


@admin.register(FastestGrowingMarket)
class FastestGrowingMarketAdmin(admin.ModelAdmin):
    list_display = ["rank", "location", "change_display"]
    list_display_links = ["location"]
    list_editable = ["rank"]
