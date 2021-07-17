from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

user_urlpatterns = [
    path("sign-up/", views.SignupAPIView.as_view(), name="sign-up"),
    path("sign-in/", obtain_auth_token, name="sign-in"),
    path("user/", views.UserDetailsAPIView.as_view(), name="details"),
]

wallet_urlpatterns = [
    path("deposit/", views.DepositMoneyAPIView.as_view(), name="deposit"),
    path("transfer/", views.TransferMoneyAPIView.as_view(), name="transfer"),
]

urlpatterns = [
    path("", include((user_urlpatterns, "user"))),
    path("wallet/", include((wallet_urlpatterns, "wallet"))),
]
