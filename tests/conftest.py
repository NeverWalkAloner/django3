import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from payments.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username="yoda", password="use_force")


@pytest.fixture
def second_user():
    return User.objects.create_user(username="luke", password="family_first")


@pytest.fixture
def wallet_with_money(user):
    user.wallet.balance = 100
    user.wallet.save()
    return user.wallet


@pytest.fixture
def user_token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def authenticated_client(user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {user_token.key}")
    return client
