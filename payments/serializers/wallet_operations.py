from rest_framework import serializers

from ..models import Transaction, Wallet


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["amount", "comment"]


class TransferSerializer(serializers.ModelSerializer):
    to_wallet = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Wallet.objects.all()
    )

    class Meta:
        model = Transaction
        fields = ["to_wallet", "amount", "comment"]
