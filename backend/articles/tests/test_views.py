from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from articles.models import Article
import datetime


def make_article(**kwargs):
    defaults = {
        "slug": "test-article",
        "title": "Test Article",
        "headline": "Test Headline",
        "category": Article.Category.NOTABLE_SALE,
        "body": "Body text.",
        "byline": "By Test Author",
        "published_date": datetime.date(2024, 5, 12),
    }
    defaults.update(kwargs)
    return Article.objects.create(**defaults)


class ArticleListViewTest(APITestCase):
    def test_returns_200(self):
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_only_published_articles(self):
        make_article(slug="published", status=Article.Status.PUBLISHED)
        make_article(slug="draft", status=Article.Status.DRAFT)
        response = self.client.get("/api/articles/")
        slugs = [a["slug"] for a in response.data["results"]]
        self.assertIn("published", slugs)
        self.assertNotIn("draft", slugs)

    def test_filter_by_category(self):
        make_article(slug="notable", category=Article.Category.NOTABLE_SALE)
        make_article(slug="pulse", category=Article.Category.MARKET_PULSE)
        response = self.client.get("/api/articles/?category=NOTABLE_SALE")
        slugs = [a["slug"] for a in response.data["results"]]
        self.assertIn("notable", slugs)
        self.assertNotIn("pulse", slugs)

    def test_list_fields_present(self):
        make_article()
        response = self.client.get("/api/articles/")
        article = response.data["results"][0]
        expected_fields = {"slug", "headline", "category", "byline", "hero_image_url", "published_date", "is_featured"}
        self.assertTrue(expected_fields.issubset(article.keys()))

    def test_body_not_in_list_response(self):
        make_article()
        response = self.client.get("/api/articles/")
        self.assertNotIn("body", response.data["results"][0])


class ArticleDetailViewTest(APITestCase):
    def test_returns_200_for_valid_slug(self):
        make_article(slug="naples-bayfront-estate")
        response = self.client.get("/api/articles/naples-bayfront-estate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_unknown_slug(self):
        response = self.client.get("/api/articles/does-not-exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_404_for_unpublished(self):
        make_article(slug="draft-article", status=Article.Status.DRAFT)
        response = self.client.get("/api/articles/draft-article/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_includes_body(self):
        make_article(slug="full-article", body="Full article body here.")
        response = self.client.get("/api/articles/full-article/")
        self.assertEqual(response.data["body"], "Full article body here.")


class FeaturedArticleViewTest(APITestCase):
    def test_returns_featured_article_when_present(self):
        make_article(slug="regular")
        make_article(slug="featured", is_featured=True)
        response = self.client.get("/api/articles/featured/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], "featured")

    def test_falls_back_to_first_article_when_none_featured(self):
        make_article(slug="only-article")
        response = self.client.get("/api/articles/featured/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], "only-article")

    def test_returns_404_when_no_articles_exist(self):
        response = self.client.get("/api/articles/featured/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
