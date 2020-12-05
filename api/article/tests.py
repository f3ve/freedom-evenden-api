"""
Article Tests
"""

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api import test_helpers


class ArticleListTestCase(APITestCase):
    """
    Test POST and GET articles
    """
    url = reverse("articles")
    client = APIClient()

    def test_post_article(self):
        """
        Should return 201 and new article
        """

        user = test_helpers.create_test_user(0)
        article = test_helpers.test_article1
        response = self.client.post(self.url, article)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
