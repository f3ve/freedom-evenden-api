from rest_framework import serializers
from api.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    generic serializer for user model
    """

    password = serializers.CharField(write_only=True)

    class meta:
        model = User
        fields = ["username", "email", "full_name"]
