from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


User = get_user_model()


class ProductTests(APITestCase):
    def test_product_list_public(self):
        """Test public can view products"""
        Product.objects.create(name="Item", description="Test", price=10, stock=5)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_create_requires_admin(self):
        """Test only admins can create products"""
        user = User.objects.create_user(username="alice", password="pass12345")
        self.client.force_authenticate(user)
        response = self.client.post(
            "/api/products/",
            {"name": "New Product", "price": "20.00", "stock": 10},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_create_admin(self):
        """Test admins can create products"""
        admin = User.objects.create_superuser(username="admin", password="admin123")
        self.client.force_authenticate(admin)
        response = self.client.post(
            "/api/products/",
            {"name": "Admin Product", "description": "Test", "price": "30.00", "stock": 15},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
