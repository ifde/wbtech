from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.products.models import Product

from .models import Cart, CartItem


def get_or_create_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@transaction.atomic
def add_item(user, product_id: int, quantity: int) -> Cart:
    cart = get_or_create_cart(user)
    product = get_object_or_404(Product, id=product_id)
    
    if quantity > product.stock:
        raise ValidationError(f"Only {product.stock} items in stock.")
    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = quantity
    else:
        total = item.quantity + quantity
        if total > product.stock:
            raise ValidationError(f"Only {product.stock - item.quantity} more items available.")
        item.quantity = total
    item.save(update_fields=["quantity"])
    return cart


@transaction.atomic
def remove_item(user, product_id: int) -> Cart:
    cart = get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return cart


@transaction.atomic
def update_item(user, product_id: int, quantity: int) -> Cart:
    cart = get_or_create_cart(user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    
    if quantity > item.product.stock:
        raise ValidationError(f"Only {item.product.stock} items in stock.")
    
    if quantity <= 0:
        item.delete()
        return cart
    
    item.quantity = quantity
    item.save(update_fields=["quantity"])
    return cart
