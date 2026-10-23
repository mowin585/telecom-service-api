from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from customers.models import Customer
from services.models import Service
from .models import Subscription


class SubscriptionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="subscription_test_user",
            password="testpassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        self.customer = Customer.objects.create(
            full_name="Test Customer",
            phone_number="0712345678",
            email="testcustomer@example.com",
        )

        self.service = Service.objects.create(
            name="Test Data Bundle",
            service_type="DATA",
            price="10000.00",
            validity_days=7,
        )

        self.subscription = Subscription.objects.create(
            customer=self.customer,
            service=self.service,
            end_date=timezone.now() + timedelta(days=7),
            status="ACTIVE",
        )


    def test_list_subscriptions(self):
        response = self.client.get("/api/subscriptions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_customer(self):
        response = self.client.get(
            f"/api/subscriptions/?customer={self.customer.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_status(self):
        response = self.client.get(
            "/api/subscriptions/?status=ACTIVE"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_cancel_subscription(self):
        response = self.client.delete(
            f"/api/subscriptions/{self.subscription.id}/"
        )
        self.assertEqual(response.status_code, 200)

        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.status, "CANCELLED")

    def test_expire_overdue_subscription(self):
        self.subscription.end_date = timezone.now() - timedelta(days=1)
        self.subscription.save(update_fields=["end_date"])

        response = self.client.get("/api/subscriptions/")

        self.assertEqual(response.status_code, 200)

        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.status, "EXPIRED")
