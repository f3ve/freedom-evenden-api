"""
Article Views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.article import serializers
from api.models import Article


class ArticlesView(APIView):
    """
    POST, GET users
    """

    def post(self, request):
        """
        returns a list of public articles
        """
        serializer = serializers.ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
