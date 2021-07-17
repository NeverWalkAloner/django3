from decimal import Decimal
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError


class UserWithWalletManager(UserManager):
    @transaction.atomic
    def create_user(self, username, email=None, password=None, **extra_fields):
        # override create_user to make sure that
        # a new wallet created for the user in single transaction
        user = super().create_user(username, email, password, **extra_fields)
        Wallet.objects.create(owner=user)
        return user


class User(AbstractUser):
    """
    Use custom user model so that we can
    override manager and extend it in the future
    """
    objects = UserWithWalletManager()


class Wallet(models.Model):
    owner = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        related_name="wallet",
        on_delete=models.CASCADE
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # unique identifier shown for the user if necessary
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    class Meta:
        # last defence against negative balance
        # If we want to allow negative balance we can remove constraint
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte=0),
                                   name="positive_balance"),
        ]

    def withdraw_money(self, amount: Decimal) -> None:
        # this check is prone to a race-condition
        # that's why we added DB constraint as well
        if self.balance < amount:
            raise ValidationError("Not enough money")
        # use F() here to protect against race-condition while updating
        self.balance = models.F("balance") - amount
        self.save(update_fields=["balance"])

    def deposit_money(self, amount: Decimal) -> None:
        # use F() here to protect against race-condition while updating
        self.balance = models.F("balance") + amount
        self.save(update_fields=["balance"])
