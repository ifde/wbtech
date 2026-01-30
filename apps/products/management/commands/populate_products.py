from django.core.management.base import BaseCommand
from apps.products.models import Product


class Command(BaseCommand):
    help = "Populate database with sample products"

    def handle(self, *args, **kwargs):
        products = [
            {
                "name": "Wireless Headphones",
                "description": "High-quality Bluetooth headphones with noise cancellation",
                "price": "79.99",
                "stock": 25,
            },
            {
                "name": "Smart Watch",
                "description": "Fitness tracker with heart rate monitor and GPS",
                "price": "199.99",
                "stock": 15,
            },
            {
                "name": "Laptop Stand",
                "description": "Adjustable aluminum laptop stand for ergonomic setup",
                "price": "34.99",
                "stock": 50,
            },
            {
                "name": "USB-C Hub",
                "description": "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader",
                "price": "45.99",
                "stock": 30,
            },
            {
                "name": "Mechanical Keyboard",
                "description": "RGB mechanical keyboard with blue switches",
                "price": "129.99",
                "stock": 20,
            },
            {
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse with customizable buttons",
                "price": "29.99",
                "stock": 40,
            },
            {
                "name": "Webcam HD",
                "description": "1080p HD webcam with built-in microphone",
                "price": "59.99",
                "stock": 18,
            },
            {
                "name": "Phone Case",
                "description": "Protective silicone case with shock absorption",
                "price": "12.99",
                "stock": 100,
            },
            {
                "name": "Portable Charger",
                "description": "20000mAh power bank with fast charging",
                "price": "39.99",
                "stock": 35,
            },
            {
                "name": "Screen Protector",
                "description": "Tempered glass screen protector pack of 2",
                "price": "9.99",
                "stock": 80,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product_data["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product_data["name"]}')
                )

        self.stdout.write(self.style.SUCCESS(f"\nTotal products in database: {Product.objects.count()}"))
