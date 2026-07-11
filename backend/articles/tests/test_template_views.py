"""
Template view tests — one test class per view.

Pattern: each test class has a setUp() that creates the minimum DB objects
needed, then tests check status codes, correct templates, context variables,
and that key text actually appears in the rendered HTML.
"""
from django.test import TestCase
from django.urls import reverse
from articles.models import Article
import datetime


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_article(**kwargs):
    """
    Factory for Article objects. Provides sensible defaults so individual
    tests only need to override the fields they care about.
    """
    defaults = {
        "slug": "test-article",
        "title": "Test Article",
        "headline": "Test Headline",
        "subheadline": "Test subheadline",
        "category": Article.Category.MARKET_PULSE,
        "body": "Body text.",
        "byline": "Staff Writer",
        "published_date": datetime.date.today(),
        "is_featured": False,
        "is_published": True,
    }
    defaults.update(kwargs)
    return Article.objects.create(**defaults)


# ── Step 4: base template loads ───────────────────────────────────────────────

class BaseTemplateTest(TestCase):
    """
    The home URL must use base.html as its parent template.
    This is the first minimal test — just proves the URL exists and
    the template inheritance chain is wired up.
    """

    def test_home_uses_base_template(self):
        # reverse('home') looks up the URL named 'home' in urls.py
        response = self.client.get(reverse("home"))
        # assertTemplateUsed checks that the named template was rendered
        self.assertTemplateUsed(response, "base.html")


# ── Step 5: home page ─────────────────────────────────────────────────────────

class HomeViewTest(TestCase):
    """
    Tests for the home page view. Creates a featured article so the
    view has something to show in the hero section.
    """

    def setUp(self):
        # setUp() runs before every test in this class — creates fresh DB objects
        self.featured = make_article(
            slug="featured-article",
            headline="Featured Headline",
            is_featured=True,
        )

    def test_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        # home.html should extend base.html — both should be reported as used
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_featured_article_in_context(self):
        # The view must pass 'featured' to the template context
        response = self.client.get(reverse("home"))
        self.assertIsNotNone(response.context["featured"])

    def test_featured_headline_renders(self):
        # The featured article's headline must appear somewhere in the HTML
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Featured Headline")

    def test_articles_in_context(self):
        # The view must pass an 'articles' list for the card row
        response = self.client.get(reverse("home"))
        self.assertIn("articles", response.context)


# ── Step 6: article detail page ───────────────────────────────────────────────

class ArticleDetailViewTest(TestCase):
    """
    Tests for /articles/<slug>/ — individual article page.
    """

    def setUp(self):
        self.article = make_article(
            slug="my-article",
            headline="My Article Headline",
            category=Article.Category.AGENT_WATCH,
        )

    def test_returns_200(self):
        # reverse('article_detail', args=['my-article']) → /articles/my-article/
        response = self.client.get(reverse("article_detail", args=["my-article"]))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_missing_slug(self):
        response = self.client.get(reverse("article_detail", args=["does-not-exist"]))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("article_detail", args=["my-article"]))
        self.assertTemplateUsed(response, "article_detail.html")

    def test_headline_renders(self):
        response = self.client.get(reverse("article_detail", args=["my-article"]))
        self.assertContains(response, "My Article Headline")

    def test_article_in_context(self):
        response = self.client.get(reverse("article_detail", args=["my-article"]))
        self.assertEqual(response.context["article"], self.article)
