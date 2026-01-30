from django.urls import path

from .views import RegisterView, ProfileView, BalanceTopUpView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("balance/topup/", BalanceTopUpView.as_view(), name="balance_topup"),
]
