from decimal import Decimal
import pytest

from django.urls import reverse

from rest_framework import status


@pytest.mark.django_db
def test_signup_success_response(client):
    url = reverse("user:sign-up")
    data = {
        "username": "vader",
        "password": "best_daddy_ever",
        "email": "vader@deathstar.com",
        "first_name": "Anakin",
        "last_name": "Skywalker"
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "vader"
    assert response.data["email"] == "vader@deathstar.com"
    assert response.data["first_name"] == "Anakin"
    assert response.data["last_name"] == "Skywalker"
    assert "wallet_uuid" in response.data
    assert "password" not in response.data


@pytest.mark.django_db
def test_signup_bad_request_response(client):
    url = reverse("user:sign-up")
    data = {
        "email": "vader@deathstar.com",
        "first_name": "Anakin",
        "last_name": "Skywalker"
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_deposit_unauthorized_response(client):
    url = reverse("wallet:deposit")
    data = {
        "amount": "42.00",
        "comment": "Don't panic!",
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_deposit_negative_amount_bad_request_response(authenticated_client):
    url = reverse("wallet:deposit")
    data = {
        "amount": "-42.00",
        "comment": "Don't panic!",
    }

    response = authenticated_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "amount" in response.data


@pytest.mark.django_db
def test_deposit_does_not_round_amount(authenticated_client):
    url = reverse("wallet:deposit")
    data = {
        "amount": "42.001",
        "comment": "Don't panic!",
    }

    response = authenticated_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "amount" in response.data


@pytest.mark.django_db
def test_deposit_success_response(authenticated_client, user):
    url = reverse("wallet:deposit")
    data = {
        "amount": "42.00",
        "comment": "Don't panic!",
    }

    response = authenticated_client.post(url, data=data)
    user.refresh_from_db()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["amount"] == "42.00"
    assert response.data["comment"] == "Don't panic!"
    assert user.wallet.balance == Decimal("42.00")
    assert user.wallet.incomes.count() == 1


@pytest.mark.django_db
def test_transfer_success_response(
        authenticated_client, user, second_user, wallet_with_money
):
    url = reverse("wallet:transfer")
    data = {
        "amount": "42.00",
        "comment": "Don't panic!",
        "to_wallet": second_user.wallet.uuid,
    }

    response = authenticated_client.post(url, data=data)
    user.refresh_from_db()
    second_user.refresh_from_db()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["amount"] == "42.00"
    assert response.data["comment"] == "Don't panic!"
    assert user.wallet.balance == Decimal("58.00")
    assert user.wallet.expenses.count() == 1
    assert second_user.wallet.balance == Decimal("42.00")
    assert second_user.wallet.incomes.count() == 1


@pytest.mark.django_db
def test_transfer_unauthorized_response(client, second_user):
    url = reverse("wallet:transfer")
    data = {
        "amount": "42.00",
        "comment": "Don't panic!",
        "to_wallet": second_user.wallet.uuid,
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_transfer_bad_request_response(
        authenticated_client, user, second_user, wallet_with_money
):
    url = reverse("wallet:transfer")
    data = {
        "amount": "420.00",
        "comment": "Don't panic!",
        "to_wallet": second_user.wallet.uuid,
    }

    response = authenticated_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Not enough money" in str(response.data["message"])


@pytest.mark.django_db
def test_user_details_success_response(authenticated_client, user):
    url = reverse("user:details")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name
    assert response.data["wallet_uuid"] == str(user.wallet.uuid)
    assert Decimal(response.data["balance"]) == user.wallet.balance
