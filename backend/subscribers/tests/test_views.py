from rest_framework.test import APITestCase
from rest_framework import status
from subscribers.models import Subscriber


class SubscribeViewTest(APITestCase):
    def test_new_subscriber_returns_201(self):
        response = self.client.post("/api/subscribers/", {"email": "new@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Subscribed successfully.")

    def test_new_subscriber_is_saved_to_db(self):
        self.client.post("/api/subscribers/", {"email": "saved@example.com"}, format="json")
        self.assertTrue(Subscriber.objects.filter(email="saved@example.com").exists())

    def test_duplicate_email_returns_200_not_400(self):
        Subscriber.objects.create(email="existing@example.com")
        response = self.client.post("/api/subscribers/", {"email": "existing@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Already subscribed.")

    def test_duplicate_does_not_create_second_record(self):
        Subscriber.objects.create(email="once@example.com")
        self.client.post("/api/subscribers/", {"email": "once@example.com"}, format="json")
        self.assertEqual(Subscriber.objects.filter(email="once@example.com").count(), 1)

    def test_invalid_email_returns_400(self):
        response = self.client.post("/api/subscribers/", {"email": "not-an-email"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_is_lowercased_on_save(self):
        self.client.post("/api/subscribers/", {"email": "Upper@Example.COM"}, format="json")
        self.assertTrue(Subscriber.objects.filter(email="upper@example.com").exists())
