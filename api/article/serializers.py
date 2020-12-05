"""
Article Serializers
"""

from rest_framework import serializers
from api.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    generic serializer for Article model
    """

    class Meta:
        model = Article
        fields = '__all__'
