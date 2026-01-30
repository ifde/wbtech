from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Product
from .models import CartItem


User = get_user_model()


class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass12345")
        self.product = Product.objects.create(name="Item", description="Test", price=10, stock=5)
        self.client.force_authenticate(self.user)

    def test_add_to_cart(self):
        """Test adding product to cart"""
        response = self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 1)
        item = CartItem.objects.first()
        self.assertEqual(item.quantity, 2)

    def test_remove_from_cart(self):
        """Test removing product from cart"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 1})
        response = self.client.post("/api/cart/remove/", {"product_id": self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_update_cart_quantity(self):
        """Test updating cart item quantity"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 1})
        response = self.client.post("/api/cart/update/", {"product_id": self.product.id, "quantity": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = CartItem.objects.first()
        self.assertEqual(item.quantity, 5)

    def test_view_cart(self):
        """Test viewing cart contents"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 3})
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
