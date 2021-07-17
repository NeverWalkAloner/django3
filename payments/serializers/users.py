from rest_framework import serializers

from ..models import User


class SignupSerializer(serializers.ModelSerializer):
    # read_only field used to show user his wallet details
    wallet_uuid = serializers.UUIDField(source="wallet.uuid", read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "wallet_uuid",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> User:
        # create_user in used to make sure that the password was hashed
        # and a wallet was created
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    wallet_uuid = serializers.UUIDField(source="wallet.uuid")
    balance = serializers.UUIDField(source="wallet.balance")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "wallet_uuid",
            "balance",
        ]