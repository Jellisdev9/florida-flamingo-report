"""
Template view tests for the Notable Sales page.
"""
from django.test import TestCase
from django.urls import reverse
from sales.models import NotableSale
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
        # ?region=ORLANDO should not show our South Florida sale
        response = self.client.get(reverse("notable_sales") + "?region=ORLANDO")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Bayfront Estate")

    def test_region_filter_shows_matching_region(self):
        # ?region=SOUTH_FLORIDA should show our sale
        response = self.client.get(reverse("notable_sales") + "?region=SOUTH_FLORIDA")
        self.assertContains(response, "Bayfront Estate")

    def test_sales_in_context(self):
        response = self.client.get(reverse("notable_sales"))
        self.assertIn("sales", response.context)
