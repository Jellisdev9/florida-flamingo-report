from django.test import TestCase
from django.db import IntegrityError
from subscribers.models import Subscriber


class SubscriberModelTest(TestCase):
    def test_str_returns_email(self):
        s = Subscriber.objects.create(email="test@example.com")
        self.assertEqual(str(s), "test@example.com")

    def test_email_must_be_unique(self):
        Subscriber.objects.create(email="dup@example.com")
        with self.assertRaises(IntegrityError):
            Subscriber.objects.create(email="dup@example.com")

    def test_is_active_defaults_to_true(self):
        s = Subscriber.objects.create(email="active@example.com")
        self.assertTrue(s.is_active)

    def test_subscribed_at_is_set_on_create(self):
        s = Subscriber.objects.create(email="timestamped@example.com")
        self.assertIsNotNone(s.subscribed_at)
