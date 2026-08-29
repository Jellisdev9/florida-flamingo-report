"""
Template view tests for the Market Pulse, Agents, and Neighborhoods pages.
"""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from articles.models import Article
from market.models import Agent, NeighborhoodIntel


def make_article(**kwargs):
    defaults = {
        "slug": "test-article",
        "title": "Test Article",
        "headline": "Test Headline",
        "category": Article.Category.MARKET_PULSE,
        "body": "Body text.",
        "byline": "Staff Writer",
        "published_date": timezone.now().date(),
        "status": Article.Status.PUBLISHED,
    }
    defaults.update(kwargs)
    return Article.objects.create(**defaults)


def make_agent(**kwargs):
    now = timezone.now()
    defaults = {
        "name": "Test Agent",
        "location": "Miami",
        "volume_display": "$10M",
        "rank": 1,
        "period_month": now.month,
        "period_year": now.year,
    }
    defaults.update(kwargs)
    return Agent.objects.create(**defaults)


def make_neighborhood(**kwargs):
    defaults = {
        "neighborhood": "Winter Park",
        "city": "Orlando",
        "description": "Inventory tightens.",
        "tag": NeighborhoodIntel.Tag.HOT,
    }
    defaults.update(kwargs)
    return NeighborhoodIntel.objects.create(**defaults)


class MarketPulseViewTest(TestCase):
    def setUp(self):
        self.article = make_article(
            slug="market-pulse-article",
            headline="Market Pulse Headline",
            category=Article.Category.MARKET_PULSE,
        )
        # Should not appear — wrong category
        make_article(slug="other-article", headline="Agent Watch Headline", category=Article.Category.AGENT_WATCH)

    def test_returns_200(self):
        response = self.client.get(reverse("market_pulse"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("market_pulse"))
        self.assertTemplateUsed(response, "market_pulse.html")

    def test_market_pulse_article_renders(self):
        response = self.client.get(reverse("market_pulse"))
        self.assertContains(response, "Market Pulse Headline")

    def test_excludes_other_categories(self):
        response = self.client.get(reverse("market_pulse"))
        self.assertNotContains(response, "Agent Watch Headline")


class AgentsViewTest(TestCase):
    def setUp(self):
        self.agent = make_agent(name="Current Period Agent")
        self.watch_article = make_article(
            slug="agent-watch-article",
            headline="Agent Watch Headline",
            category=Article.Category.AGENT_WATCH,
        )

    def test_returns_200(self):
        response = self.client.get(reverse("agents"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("agents"))
        self.assertTemplateUsed(response, "agents.html")

    def test_agent_renders(self):
        response = self.client.get(reverse("agents"))
        self.assertContains(response, "Current Period Agent")

    def test_agent_watch_article_renders(self):
        response = self.client.get(reverse("agents"))
        self.assertContains(response, "Agent Watch Headline")

    def test_falls_back_to_all_agents_when_no_current_period(self):
        Agent.objects.all().delete()
        make_agent(name="Old Period Agent", period_month=1, period_year=2020)
        response = self.client.get(reverse("agents"))
        self.assertContains(response, "Old Period Agent")


class NeighborhoodsViewTest(TestCase):
    def setUp(self):
        self.neighborhood = make_neighborhood(neighborhood="Winter Park")
        self.watch_article = make_article(
            slug="neighborhood-watch-article",
            headline="Neighborhood Watch Headline",
            category=Article.Category.NEIGHBORHOOD_WATCH,
        )

    def test_returns_200(self):
        response = self.client.get(reverse("neighborhoods"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("neighborhoods"))
        self.assertTemplateUsed(response, "neighborhoods.html")

    def test_neighborhood_renders(self):
        response = self.client.get(reverse("neighborhoods"))
        self.assertContains(response, "Winter Park")

    def test_neighborhood_watch_article_renders(self):
        response = self.client.get(reverse("neighborhoods"))
        self.assertContains(response, "Neighborhood Watch Headline")
