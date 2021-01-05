"""
Category serializers
"""

from rest_framework.serializers import ModelSerializer
from api.models import Category


class CategorySerializer(ModelSerializer):

    """
    generic serializer for Category model
    """

    class Meta:
        model = Category
        fields = '__all__'
