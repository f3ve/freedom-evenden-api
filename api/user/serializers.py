"""
Serializers for user model
"""

from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    generic serializer for user model
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "full_name", "password", "id"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
