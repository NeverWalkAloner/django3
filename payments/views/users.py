from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from ..serializers.users import SignupSerializer, UserSerializer


class SignupAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer


class UserDetailsAPIView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
