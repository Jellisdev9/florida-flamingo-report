from rest_framework.test import APITestCase
from rest_framework import status
from sales.models import NotableSale
import datetime


def make_sale(**kwargs):
    defaults = {
        "slug": "test-sale",
        "title": "Test Sale",
        "price": 5000000,
        "location": "123 Ocean Dr",
        "city": "Miami Beach",
        "region": NotableSale.Region.SOUTH_FLORIDA,
        "property_type": NotableSale.PropertyType.WATERFRONT_ESTATE,
        "close_date": datetime.date(2024, 5, 12),
    }
    defaults.update(kwargs)
    return NotableSale.objects.create(**defaults)


class NotableSaleListViewTest(APITestCase):
    def test_returns_200(self):
        response = self.client.get("/api/sales/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_region(self):
        make_sale(slug="south", region=NotableSale.Region.SOUTH_FLORIDA)
        make_sale(slug="tampa", region=NotableSale.Region.TAMPA_BAY)
        response = self.client.get("/api/sales/?region=SOUTH_FLORIDA")
        slugs = [s["slug"] for s in response.data["results"]]
        self.assertIn("south", slugs)
        self.assertNotIn("tampa", slugs)

    def test_filter_by_property_type(self):
        make_sale(slug="waterfront", property_type=NotableSale.PropertyType.WATERFRONT_ESTATE)
        make_sale(slug="commercial", property_type=NotableSale.PropertyType.COMMERCIAL)
        response = self.client.get("/api/sales/?property_type=COMMERCIAL")
        slugs = [s["slug"] for s in response.data["results"]]
        self.assertIn("commercial", slugs)
        self.assertNotIn("waterfront", slugs)

    def test_response_includes_price_display(self):
        make_sale(price=32500000)
        response = self.client.get("/api/sales/")
        self.assertIn("price_display", response.data["results"][0])
        self.assertEqual(response.data["results"][0]["price_display"], "$32,500,000")


class FeaturedSaleViewTest(APITestCase):
    def test_returns_featured_sale(self):
        make_sale(slug="not-featured", is_featured=False)
        make_sale(slug="featured-sale", is_featured=True)
        response = self.client.get("/api/sales/featured/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], "featured-sale")

    def test_returns_404_when_none_featured(self):
        response = self.client.get("/api/sales/featured/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TopClosingsViewTest(APITestCase):
    def test_returns_top_5_by_price(self):
        for i, price in enumerate([10, 20, 30, 40, 50, 60]):
            make_sale(slug=f"sale-{i}", price=price * 1_000_000)
        response = self.client.get("/api/sales/top-closings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        prices = [s["price_display"] for s in response.data]
        self.assertEqual(prices[0], "$60,000,000")
