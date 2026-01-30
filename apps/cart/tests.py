from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Product


User = get_user_model()


class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass12345")
        self.product = Product.objects.create(name="Item", description="Test", price=10, stock=5)

    def test_add_to_cart(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
