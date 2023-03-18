import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user."""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        read_only_fields = ["id", "date_joined", "date_updated"]
        fields = [
            'id',
            'username',
            'phone_number',
            'birthday',
            'email',
            'password',
        ]

    def validate_password(self, value):
        """Validate whether the password contains minimum one digit
        and contains minimum 8 symbols.

        """
        if not re.match(r'^((?=.*?[0-9]).*).{8,}$', value):
            raise ValidationError(
                "Пароль должен содержать не менее 8 символов,"
                "из которых хотя бы одна цифра.",
                code='password_is_weak',
            )
        return value

    def create(self, validated_data: dict) -> User:
        """Create a new User instance hashing the password."""
        password = validated_data['password']

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update a User instance hashing the password."""
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for displaying users."""

    class Meta:
        model = User
        read_only_fields = ["id", "date_joined", "date_updated"]
        fields = [
            'id',
            'username',
            'phone_number',
            'birthday',
            'email',
            'is_staff',
            'date_joined',
            'date_updated',
        ]
