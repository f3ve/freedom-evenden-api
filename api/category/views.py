"""
Category Views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.category import serializers
from api.models import Category


class CategoryView(APIView):
    """
    POST, GET categories
    """

    def get(self, request):
        """
        returns a list of all categories
        """
        categories = Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
