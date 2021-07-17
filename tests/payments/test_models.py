import decimal
import pytest

from django.core.exceptions import ValidationError

from payments.models.user import User


@pytest.mark.django_db
def test_create_user_with_wallet():
    user = User.objects.create_user(
        username="darth", password="best_daddy_ever"
    )

    assert user.wallet is not None
    assert user.wallet.balance == decimal.Decimal("0")


@pytest.mark.django_db
def test_withdraw_money(wallet_with_money):
    wallet_with_money.withdraw_money(decimal.Decimal("42.0"))
    wallet_with_money.refresh_from_db()

    assert wallet_with_money.balance == decimal.Decimal("58.0")


@pytest.mark.django_db
def test_withdraw_too_much_money(wallet_with_money):
    with pytest.raises(ValidationError):
        wallet_with_money.withdraw_money(decimal.Decimal("420.0"))


@pytest.mark.django_db
def test_deposit_money(wallet_with_money):
    wallet_with_money.deposit_money(decimal.Decimal("42.0"))
    wallet_with_money.refresh_from_db()

    assert wallet_with_money.balance == decimal.Decimal("142.0")