"""
Article Views
"""
import datetime
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

    def get(self, request):
        """
        returns a list of published articles ordered from most recent to oldest
        """
        today = datetime.date.today()
        articles = Article.objects.filter(
            draft=False, publish_date__lte=today).order_by('-publish_date')
        serializer = serializers.ArticleSerializer(articles, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ArticleDetailView(APIView):
    """
    GET, PATCH, DELETE
    """

    def get_object(self, pk, call_back):
        """
        attemps to fetch specified article, returns 404 if article not found
        """

        try:
            article = Article.objects.get(slug=pk)
            return call_back(article)
        except Article.DoesNotExist:
            return Response({"message": "Article does not exist"}, status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """
        returns specified article
        """

        def return_article(article):
            serializer = serializers.ArticleSerializer(article)
            return Response(serializer.data)

        return self.get_object(pk, return_article)

    def patch(self, request, pk):
        """
        PATCH fields in specified article
        """

        def update_article(article):
            serializer = serializers.ArticleSerializer(
                article, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return self.get_object(pk, update_article)

    def delete(self, request, pk):
        """
        deletes specified user
        """
        def delete_article(article):
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.get_object(pk, delete_article)
