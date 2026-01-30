from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


User = get_user_model()


class ProductTests(APITestCase):
    def test_product_list_public(self):
        Product.objects.create(name="Item", description="Test", price=10, stock=5)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
