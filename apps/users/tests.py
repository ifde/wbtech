from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def test_user_registration_and_profile(self):
        register_url = reverse("register")
        response = self.client.post(
            register_url,
            {"username": "alice", "password": "pass12345", "email": "a@example.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
