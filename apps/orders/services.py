import logging
from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.cart.models import Cart

from .models import Order, OrderItem


logger = logging.getLogger("orders")


@transaction.atomic
def create_order_from_cart(user) -> Order:
    cart = Cart.objects.prefetch_related("items__product").filter(user=user).first()
    if not cart or not cart.items.exists():
        raise ValidationError("Cart is empty.")

    items = list(cart.items.all())
    total = Decimal("0.00")

    for item in items:
        if item.quantity > item.product.stock:
            raise ValidationError(f"Not enough stock for {item.product.name}.")
        total += item.product.price * item.quantity

    if user.balance < total:
        raise ValidationError("Insufficient balance.")

    user.balance -= total
    user.save(update_fields=["balance"])

    order = Order.objects.create(user=user, total_amount=total)

    for item in items:
        product = item.product
        product.stock -= item.quantity
        product.save(update_fields=["stock"])
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=item.quantity,
        )

    cart.items.all().delete()

    logger.info("=" * 80)
    logger.info("✅ ORDER CREATED SUCCESSFULLY")
    logger.info("Order ID: %s", order.id)
    logger.info("User: %s (ID: %s)", user.username, user.id)
    logger.info("Total Amount: $%s", total)
    logger.info("Items: %s", ", ".join([f"{item.product.name} x{item.quantity}" for item in order.items.all()]))
    logger.info("New User Balance: $%s", user.balance)
    logger.info("=" * 80)

    return order
