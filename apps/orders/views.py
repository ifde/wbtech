from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import OrderSerializer
from .services import create_order_from_cart
from .models import Order


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = Order.objects.filter(user=request.user, pk=pk).first()
        if not order:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializer(order).data)

    def create(self, request):
        order = create_order_from_cart(request.user)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
