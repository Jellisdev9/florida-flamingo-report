from django.test import TestCase
from django.db import IntegrityError
from articles.models import Article
import datetime


def make_article(**kwargs):
    defaults = {
        "slug": "test-article",
        "title": "Test Article",
        "headline": "Test Headline",
        "category": Article.Category.NOTABLE_SALE,
        "body": "Article body text.",
        "byline": "By Test Author",
        "published_date": datetime.date(2024, 5, 12),
    }
    defaults.update(kwargs)
    return Article.objects.create(**defaults)


class ArticleModelTest(TestCase):
    def test_str_returns_headline(self):
        article = make_article(headline="Naples Bayfront Estate Sets Record")
        self.assertEqual(str(article), "Naples Bayfront Estate Sets Record")

    def test_slug_must_be_unique(self):
        make_article(slug="duplicate-slug")
        with self.assertRaises(IntegrityError):
            make_article(slug="duplicate-slug", title="Different Title")

    def test_default_ordering_is_newest_first(self):
        make_article(slug="older", published_date=datetime.date(2024, 1, 1))
        make_article(slug="newer", published_date=datetime.date(2024, 6, 1))
        slugs = list(Article.objects.values_list("slug", flat=True))
        self.assertEqual(slugs, ["newer", "older"])

    def test_is_published_defaults_to_true(self):
        article = make_article()
        self.assertTrue(article.is_published)

    def test_is_featured_defaults_to_false(self):
        article = make_article()
        self.assertFalse(article.is_featured)

    def test_read_time_defaults_to_three(self):
        article = make_article()
        self.assertEqual(article.read_time_minutes, 3)
