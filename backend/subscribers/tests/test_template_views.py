"""
Template view tests for the newsletter subscribe endpoint.

The template subscribe view accepts a POST with 'email' and 'next' fields,
saves the subscriber, and redirects — unlike the API view which returns JSON.
"""
from django.test import TestCase
from django.urls import reverse
from subscribers.models import Subscriber


# ── Step 8: newsletter subscribe ──────────────────────────────────────────────

class SubscribeViewTest(TestCase):
    """
    Tests for POST /subscribe/ — the HTML form subscription endpoint.
    """

    def test_post_creates_subscriber(self):
        # Posting a valid email should create a Subscriber record
        self.client.post(reverse("subscribe"), {"email": "test@example.com", "next": "/"})
        self.assertTrue(Subscriber.objects.filter(email="test@example.com").exists())

    def test_post_redirects(self):
        # After a successful POST, the view should redirect to the 'next' URL
        response = self.client.post(
            reverse("subscribe"), {"email": "test@example.com", "next": "/"}
        )
        # assertRedirects checks for a 302 → 200 chain
        self.assertRedirects(response, "/")

    def test_duplicate_email_does_not_error(self):
        # Submitting the same email twice should not raise an error — just redirect
        Subscriber.objects.create(email="dupe@example.com")
        response = self.client.post(
            reverse("subscribe"), {"email": "dupe@example.com", "next": "/"}
        )
        # Should still redirect (302), not crash (500)
        self.assertEqual(response.status_code, 302)
