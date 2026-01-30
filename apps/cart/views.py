from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import CartSerializer, CartItemChangeSerializer
from .services import get_or_create_cart, add_item, remove_item, update_item


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add")
    def add(self, request):
        serializer = CartItemChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            cart = add_item(
                request.user,
                serializer.validated_data["product_id"],
                serializer.validated_data.get("quantity", 1),
            )
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="remove")
    def remove(self, request):
        serializer = CartItemChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = remove_item(request.user, serializer.validated_data["product_id"])
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="update")
    def update_quantity(self, request):
        serializer = CartItemChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data.get("quantity")
        if quantity is None:
            return Response({"detail": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = update_item(request.user, serializer.validated_data["product_id"], quantity)
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)
