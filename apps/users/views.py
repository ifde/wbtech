from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import UserRegisterSerializer, UserProfileSerializer, BalanceTopUpSerializer
from .services import top_up_balance


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class BalanceTopUpView(generics.GenericAPIView):
    serializer_class = BalanceTopUpSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        top_up_balance(request.user, serializer.validated_data["amount"])
        profile = UserProfileSerializer(request.user)
        return Response(profile.data, status=status.HTTP_200_OK)
