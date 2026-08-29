"""
Template view tests for the Notable Sales page.
"""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from sales.models import NotableSale
from market.models import FastestGrowingMarket
import datetime


def make_sale(**kwargs):
    """
    Factory for NotableSale. Provides defaults so tests only override
    the fields they care about.
    """
    defaults = {
        "slug": "test-sale",
        "title": "Bayfront Estate",
        "price": 3500000,
        "location": "123 Bay Dr, Naples FL",
        "city": "Naples",
        "region": NotableSale.Region.SOUTH_FLORIDA,
        "property_type": NotableSale.PropertyType.WATERFRONT_ESTATE,
        "close_date": datetime.date.today(),
    }
    defaults.update(kwargs)
    return NotableSale.objects.create(**defaults)


# ── Step 7: notable sales page ────────────────────────────────────────────────

class NotableSalesViewTest(TestCase):
    """
    Tests for /notable-sales/ — the sales grid page with region filtering.
    """

    def setUp(self):
        self.sale = make_sale()

    def test_returns_200(self):
        response = self.client.get(reverse("notable_sales"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("notable_sales"))
        self.assertTemplateUsed(response, "notable_sales.html")

    def test_sale_renders(self):
        # The sale title must appear in the HTML
        response = self.client.get(reverse("notable_sales"))
        self.assertContains(response, "Bayfront Estate")

    def test_region_filter_excludes_other_regions(self):
        # ?region=ORLANDO should exclude our South Florida sale from the grid.
        # Checked via context['sales'] (the grid queryset) rather than the
        # rendered page, because "Top Luxury Closings" is a statewide sidebar
        # widget that intentionally ignores the region filter.
        response = self.client.get(reverse("notable_sales") + "?region=ORLANDO")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.sale, response.context["sales"])

    def test_region_filter_shows_matching_region(self):
        # ?region=SOUTH_FLORIDA should show our sale
        response = self.client.get(reverse("notable_sales") + "?region=SOUTH_FLORIDA")
        self.assertContains(response, "Bayfront Estate")

    def test_sales_in_context(self):
        response = self.client.get(reverse("notable_sales"))
        self.assertIn("sales", response.context)

    def test_fastest_growing_shows_only_current_period(self):
        now = timezone.now()
        current = FastestGrowingMarket.objects.create(
            location="Current Period City", change_display="+10%", rank=1,
            period_month=now.month, period_year=now.year,
        )
        FastestGrowingMarket.objects.create(
            location="Stale Period City", change_display="+5%", rank=1,
            period_month=1, period_year=2020,
        )
        response = self.client.get(reverse("notable_sales"))
        self.assertIn(current, response.context["fastest_growing"])
        self.assertNotContains(response, "Stale Period City")

    def test_fastest_growing_falls_back_to_all_when_no_current_period(self):
        FastestGrowingMarket.objects.create(
            location="Old Period City", change_display="+5%", rank=1,
            period_month=1, period_year=2020,
        )
        response = self.client.get(reverse("notable_sales"))
        self.assertContains(response, "Old Period City")
