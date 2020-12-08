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
        article = test_helpers.test_article1(user.id)
        response = self.client.post(self.url, article)
        res_json = response.json()
        if response.status_code is not status.HTTP_201_CREATED:
            print(res_json)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(res_json['author']), user.id)
        self.assertEqual(res_json['publish_date'],
                         str(article['publish_date']))
        self.assertIn('id', res_json)
        self.assertIsInstance(res_json['id'], int)

    def test_get_articles(self):
        """
        Should return 200 and list of articles
        """

        user = test_helpers.create_test_user(1)
        article1 = test_helpers.create_test_article(1, user, False)
        article2 = test_helpers.create_test_article(2, user, False)
        article3 = test_helpers.create_test_article(3, user, True)
        serializer1 = test_helpers.serializerArticle(article1).data
        serializer2 = test_helpers.serializerArticle(article2).data
        serializer3 = test_helpers.serializerArticle(article3).data

        response = self.client.get(self.url)
        data = response.json()
        if response.status_code is not status.HTTP_200_OK:
            print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], article1.title)
        self.assertEqual(data[1]['title'], article2.title)
        self.assertEqual(data[0], serializer1)
        self.assertEqual(data[1], serializer2)
        self.assertNotEqual(data[0], serializer2)
        self.assertNotEqual(data[1], serializer1)
        self.assertNotEqual(serializer3, data[0] or data[1])
        self.assertNotEqual(article3.id, data[0]['id'] or data[1]['id'])


class ArticleDetailTest(APITestCase):
    """
    Tests GET by id, PATCH, DELETE and delete
    """
