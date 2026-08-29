from rest_framework.test import APITestCase
from rest_framework import status
from market.models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket
from django.utils import timezone


class MarketMetricsViewTest(APITestCase):
    def test_returns_200(self):
        response = self.client.get("/api/market/metrics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_all_metrics_in_order(self):
        MarketMetric.objects.create(city="B", metric_label="x", value_display="x", change_display="x", sort_order=2)
        MarketMetric.objects.create(city="A", metric_label="x", value_display="x", change_display="x", sort_order=1)
        response = self.client.get("/api/market/metrics/")
        cities = [m["city"] for m in response.data]
        self.assertEqual(cities, ["A", "B"])

    def test_response_fields(self):
        MarketMetric.objects.create(
            city="Miami", metric_label="Median Price",
            value_display="$685,000", change_display="+6.2%", is_positive=True,
        )
        response = self.client.get("/api/market/metrics/")
        metric = response.data[0]
        self.assertIn("city", metric)
        self.assertIn("is_positive", metric)
        self.assertIn("change_display", metric)


class TopAgentsViewTest(APITestCase):
    def test_returns_200(self):
        response = self.client.get("/api/agents/top/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_current_month_agents_first(self):
        now = timezone.now()
        Agent.objects.create(
            name="Current Agent", location="Miami", volume_display="$10M",
            rank=1, period_month=now.month, period_year=now.year,
        )
        Agent.objects.create(
            name="Old Agent", location="Tampa", volume_display="$5M",
            rank=1, period_month=1, period_year=2020,
        )
        response = self.client.get("/api/agents/top/")
        self.assertEqual(response.data[0]["name"], "Current Agent")


class NeighborhoodIntelViewTest(APITestCase):
    def test_returns_200(self):
        response = self.client.get("/api/market/neighborhoods/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_includes_tag(self):
        NeighborhoodIntel.objects.create(
            neighborhood="Winter Park", city="Orlando",
            description="Hot market.", tag=NeighborhoodIntel.Tag.HOT,
        )
        response = self.client.get("/api/market/neighborhoods/")
        self.assertEqual(response.data[0]["tag"], "HOT")


class FastestGrowingViewTest(APITestCase):
    def test_returns_200(self):
        response = self.client.get("/api/market/fastest-growing/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_in_rank_order(self):
        FastestGrowingMarket.objects.create(
            location="B", change_display="+10%", rank=2, period_month=6, period_year=2026,
        )
        FastestGrowingMarket.objects.create(
            location="A", change_display="+15%", rank=1, period_month=6, period_year=2026,
        )
        response = self.client.get("/api/market/fastest-growing/")
        self.assertEqual(response.data[0]["location"], "A")
