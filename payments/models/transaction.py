import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    # unique identifier shown for the user if necessary
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    from_wallet = models.ForeignKey(
        to="payments.Wallet",
        on_delete=models.PROTECT,  # do not allow to delete wallet with history
        null=True,
        related_name="expenses",
    )
    to_wallet = models.ForeignKey(
        to="payments.Wallet",
        on_delete=models.PROTECT,  # do not allow to delete wallet with history
        related_name="incomes",
    )
    comment = models.CharField(blank=True, max_length=255)
