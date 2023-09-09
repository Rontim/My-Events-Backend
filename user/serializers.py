from rest_framework import serializers
from .models import UserAccount
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    TokenSerializer,
    TokenCreateSerializer
)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = "__all__"


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserAccount
        fields = "__all__"


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"
