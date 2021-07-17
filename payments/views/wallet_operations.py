from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from ..serializers.wallet_operations import (
    DepositSerializer,
    TransferSerializer,
)


class DepositMoneyAPIView(CreateAPIView):
    serializer_class = DepositSerializer

    @transaction.atomic
    def perform_create(self, serializer: DepositSerializer) -> None:
        # use transaction.atomic to ensure atomicity of operation
        to_wallet = self.request.user.wallet
        deposit = serializer.save(to_wallet=to_wallet)
        to_wallet.deposit_money(deposit.amount)


class TransferMoneyAPIView(CreateAPIView):
    serializer_class = TransferSerializer

    @transaction.atomic
    def perform_create(self, serializer: TransferSerializer) -> None:
        # use transaction.atomic to ensure atomicity of operation
        from_wallet = self.request.user.wallet
        transfer = serializer.save(from_wallet=from_wallet)
        to_wallet = transfer.to_wallet
        from_wallet.withdraw_money(transfer.amount)
        to_wallet.deposit_money(transfer.amount)

    def create(self, request, *args, **kwargs) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            # If there is not enough money ValidationError will be raised
            return Response(
                data={"message": e},
                status=status.HTTP_400_BAD_REQUEST
            )
