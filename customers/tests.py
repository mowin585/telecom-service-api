
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Customer


class CustomerAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.customer = Customer.objects.create(
            full_name="Amina John",
            phone_number="0712345678",
            email="amina@example.com"
        )

    def test_list_customers(self):
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        data = {
            "full_name": "Juma Ally",
            "phone_number": "0755555555",
            "email": "juma@example.com"
        }

        response = self.client.post(
            '/api/customers/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Customer.objects.filter(email="juma@example.com").exists()
        )

    def test_retrieve_customer(self):
        response = self.client.get(
            f'/api/customers/{self.customer.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Amina John')

    def test_invalid_email(self):
        data = {
            "full_name": "Test Customer",
            "phone_number": "0766666666",
            "email": "not-an-email"
        }

        response = self.client.post(
            '/api/customers/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_create_customer(self):
        self.client.credentials()

        data = {
            "full_name": "Unauthorized Customer",
            "phone_number": "0777777777",
            "email": "unauthorized@example.com"
        }

        response = self.client.post(
            '/api/customers/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )