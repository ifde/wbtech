from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Product


User = get_user_model()


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carl", password="pass12345", balance=Decimal("100.00"))
        self.product = Product.objects.create(name="Item", description="Test", price=10, stock=5)

    def test_create_order_from_cart(self):
        self.client.force_authenticate(self.user)
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
