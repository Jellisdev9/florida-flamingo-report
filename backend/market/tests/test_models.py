from django.test import TestCase
from django.db import IntegrityError
from market.models import MarketMetric, Agent, NeighborhoodIntel, FastestGrowingMarket


class MarketMetricModelTest(TestCase):
    def test_str(self):
        m = MarketMetric.objects.create(
            city="Miami", metric_label="Median Price",
            value_display="$685,000", change_display="+6.2%", is_positive=True,
        )
        self.assertEqual(str(m), "Miami — Median Price")

    def test_ordering_by_sort_order(self):
        MarketMetric.objects.create(city="B", metric_label="x", value_display="x", change_display="x", sort_order=2)
        MarketMetric.objects.create(city="A", metric_label="x", value_display="x", change_display="x", sort_order=1)
        first = MarketMetric.objects.first()
        self.assertEqual(first.city, "A")


class AgentModelTest(TestCase):
    def test_str(self):
        a = Agent.objects.create(
            name="The Jills Zeder Group", location="Miami Beach",
            volume_display="$98.4M", rank=1, period_month=5, period_year=2024,
        )
        self.assertEqual(str(a), "#1 The Jills Zeder Group")

    def test_rank_unique_per_period(self):
        Agent.objects.create(
            name="Agent A", location="Miami", volume_display="$1M",
            rank=1, period_month=5, period_year=2024,
        )
        with self.assertRaises(IntegrityError):
            Agent.objects.create(
                name="Agent B", location="Tampa", volume_display="$2M",
                rank=1, period_month=5, period_year=2024,
            )


class NeighborhoodIntelModelTest(TestCase):
    def test_str(self):
        n = NeighborhoodIntel.objects.create(
            neighborhood="Winter Park", city="Orlando",
            description="Inventory tightens.", tag=NeighborhoodIntel.Tag.HOT,
        )
        self.assertEqual(str(n), "Winter Park (HOT)")


class FastestGrowingMarketModelTest(TestCase):
    def test_str(self):
        m = FastestGrowingMarket.objects.create(
            location="Sarasota", change_display="+13.5%", rank=1,
            period_month=6, period_year=2026,
        )
        self.assertEqual(str(m), "#1 Sarasota — +13.5%")

    def test_rank_unique_per_period(self):
        FastestGrowingMarket.objects.create(
            location="A", change_display="+1%", rank=1, period_month=6, period_year=2026,
        )
        with self.assertRaises(IntegrityError):
            FastestGrowingMarket.objects.create(
                location="B", change_display="+2%", rank=1, period_month=6, period_year=2026,
            )

    def test_rank_can_repeat_across_periods(self):
        FastestGrowingMarket.objects.create(
            location="A", change_display="+1%", rank=1, period_month=6, period_year=2026,
        )
        # Different period — should not raise
        FastestGrowingMarket.objects.create(
            location="B", change_display="+2%", rank=1, period_month=7, period_year=2026,
        )
