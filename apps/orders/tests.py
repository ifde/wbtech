from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Product
from .models import Order


User = get_user_model()


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carl", password="pass12345", balance=Decimal("100.00"))
        self.product = Product.objects.create(name="Item", description="Test", price=10, stock=5)
        self.client.force_authenticate(self.user)

    def test_create_order_from_cart(self):
        """Test creating order from cart"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total_amount, Decimal("20.00"))

    def test_order_deducts_balance(self):
        """Test order deducts user balance"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        self.client.post("/api/orders/")
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal("80.00"))

    def test_order_deducts_stock(self):
        """Test order deducts product stock"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        self.client.post("/api/orders/")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_order_insufficient_balance(self):
        """Test order fails with insufficient balance"""
        self.user.balance = Decimal("5.00")
        self.user.save()
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 2})
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_insufficient_stock(self):
        """Test order fails with insufficient stock"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 10})
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_empty_cart(self):
        """Test order fails with empty cart"""
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders(self):
        """Test listing user orders"""
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "quantity": 1})
        self.client.post("/api/orders/")
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
