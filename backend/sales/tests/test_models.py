from django.test import TestCase
from django.db import IntegrityError
from sales.models import NotableSale
import datetime


def make_sale(**kwargs):
    defaults = {
        "slug": "test-sale",
        "title": "Test Sale",
        "price": 5000000,
        "location": "123 Ocean Dr, Miami Beach, FL",
        "city": "Miami Beach",
        "region": NotableSale.Region.SOUTH_FLORIDA,
        "property_type": NotableSale.PropertyType.WATERFRONT_ESTATE,
        "close_date": datetime.date(2024, 5, 12),
    }
    defaults.update(kwargs)
    return NotableSale.objects.create(**defaults)


class NotableSaleModelTest(TestCase):
    def test_str_includes_title_and_formatted_price(self):
        sale = make_sale(title="Boca Raton Estate", price=32500000)
        self.assertEqual(str(sale), "Boca Raton Estate — $32,500,000")

    def test_slug_must_be_unique(self):
        make_sale(slug="dup-slug")
        with self.assertRaises(IntegrityError):
            make_sale(slug="dup-slug", title="Different")

    def test_default_ordering_newest_then_highest_price(self):
        make_sale(slug="old-cheap", close_date=datetime.date(2024, 1, 1), price=1_000_000)
        make_sale(slug="new-expensive", close_date=datetime.date(2024, 6, 1), price=10_000_000)
        first = NotableSale.objects.first()
        self.assertEqual(first.slug, "new-expensive")

    def test_is_featured_defaults_to_false(self):
        sale = make_sale()
        self.assertFalse(sale.is_featured)

    def test_optional_fields_can_be_blank(self):
        sale = make_sale(brokerage="", beds=None, baths=None, sq_ft=None)
        self.assertIsNone(sale.beds)
        self.assertIsNone(sale.baths)

    def test_price_display(self):
        # price_display is a Python @property used by templates — no DB column needed
        sale = NotableSale(price=4750000)
        self.assertEqual(sale.price_display, "$4,750,000")
