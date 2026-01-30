from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserTests(APITestCase):
    def test_user_registration(self):
        """Test user registration endpoint"""
        register_url = reverse("register")
        response = self.client.post(
            register_url,
            {"username": "alice", "password": "pass12345", "email": "a@example.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "alice")

    def test_user_login(self):
        """Test JWT token obtain"""
        user = User.objects.create_user(username="bob", password="pass12345")
        response = self.client.post(
            "/api/auth/token/",
            {"username": "bob", "password": "pass12345"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_get_profile(self):
        """Test getting user profile"""
        user = User.objects.create_user(username="carl", password="pass12345")
        self.client.force_authenticate(user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "carl")
        self.assertIn("balance", response.data)

    def test_top_up_balance(self):
        """Test balance top-up"""
        user = User.objects.create_user(username="dave", password="pass12345")
        self.client.force_authenticate(user)
        response = self.client.post(
            reverse("balance_topup"),
            {"amount": "50.00"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.balance, Decimal("50.00"))
