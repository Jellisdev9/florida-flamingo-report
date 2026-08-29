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

    def test_post_lowercases_email(self):
        # unsubscribe_view lowercases its input before matching — if
        # subscribe_view doesn't normalize on save, a mixed-case signup
        # could never be found by a later (lowercase) unsubscribe request.
        self.client.post(reverse("subscribe"), {"email": "MixedCase@Example.com", "next": "/"})
        self.assertTrue(Subscriber.objects.filter(email="mixedcase@example.com").exists())

    def test_invalid_email_is_not_saved(self):
        # Unlike the API endpoint (a DRF serializer validates and 400s),
        # this view previously called Subscriber.objects.get_or_create()
        # directly, which bypasses Django's field validators entirely —
        # garbage input was silently saved. Still redirects either way
        # (matches the duplicate-email no-error UX), just shouldn't save.
        response = self.client.post(
            reverse("subscribe"), {"email": "not-an-email", "next": "/"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Subscriber.objects.filter(email="not-an-email").exists())


# ── Unsubscribe ────────────────────────────────────────────────────────────────

class UnsubscribeViewTest(TestCase):
    """
    Tests for /unsubscribe/ — the self-service unsubscribe page.

    Mirrors subscribe's trust model: no email ownership verification is
    required to subscribe, so none is required to unsubscribe either.
    """

    def test_get_returns_200(self):
        response = self.client.get(reverse("unsubscribe"))
        self.assertEqual(response.status_code, 200)

    def test_get_uses_correct_template(self):
        response = self.client.get(reverse("unsubscribe"))
        self.assertTemplateUsed(response, "unsubscribe.html")
        self.assertTemplateUsed(response, "base.html")

    def test_get_does_not_show_confirmation(self):
        response = self.client.get(reverse("unsubscribe"))
        self.assertNotContains(response, "You've been unsubscribed")

    def test_post_deactivates_matching_subscriber(self):
        subscriber = Subscriber.objects.create(email="active@example.com")
        self.client.post(reverse("unsubscribe"), {"email": "active@example.com"})
        subscriber.refresh_from_db()
        self.assertFalse(subscriber.is_active)

    def test_post_shows_confirmation(self):
        Subscriber.objects.create(email="active@example.com")
        response = self.client.post(reverse("unsubscribe"), {"email": "active@example.com"})
        self.assertContains(response, "You've been unsubscribed")

    def test_post_with_unknown_email_does_not_error(self):
        # No matching Subscriber — should still show the same confirmation,
        # not leak whether the email was ever on the list.
        response = self.client.post(reverse("unsubscribe"), {"email": "never-subscribed@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You've been unsubscribed")

    def test_post_is_case_insensitive(self):
        subscriber = Subscriber.objects.create(email="mixedcase@example.com")
        self.client.post(reverse("unsubscribe"), {"email": "MixedCase@Example.com"})
        subscriber.refresh_from_db()
        self.assertFalse(subscriber.is_active)
