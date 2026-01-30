from django.urls import path

from .views import RegisterView, ProfileView, BalanceTopUpView, APITestView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("balance/topup/", BalanceTopUpView.as_view(), name="balance_topup"),
    path("test/", APITestView.as_view(), name="api_test"),
]
