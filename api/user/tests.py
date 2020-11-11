"""
User tests
"""

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import User


class UserListTestCase(APITestCase):
    """
    Test users POST and GET
    """

    testUser1 = {
        "username": "testcase1",
        "email": "tes1t@email.com",
        "full_name": "test user",
        "password": "aaAA11!!"
    }

    invalidUser1 = {
        "username": "",
        "email": "",
        "full_name": "",
        "password": ""
    }

    users_url = reverse("users")
    client = APIClient()

    def test_post_user(self):
        """
        test user is created properly
        """
        user = self.testUser1
        url = self.users_url
        response = self.client.post(url, user)
        json_res = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(json_res, dict)
        self.assertEqual(json_res["username"], user["username"])
        self.assertEqual(json_res["email"], user["email"])
        self.assertEqual(json_res["full_name"], user["full_name"])
        self.assertIn('id', json_res)
        self.assertIsNotNone('id', json_res)
        self.assertNotIn('password', json_res)

    def test_invalid_post_user(self):
        """
        test that view handles invalid POST properly
        """
        user = self.invalidUser1
        url = self.users_url
        response = self.client.post(url, user)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for key in res_json:
            self.assertEqual(res_json[key][0], 'This field may not be blank.')

    def test_get_users_when_no_users_in_db(self):
        """
        Test GET users return empty list when no users in DB
        """
        url = self.users_url
        response = self.client.get(url)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res_json, list)
        self.assertEqual(len(res_json), 0)

    def test_get_users(self):
        """
        test GET returns list of users when users in DB
        """
        url = self.users_url

        user1 = User.objects.create_user(
            email="test3@test.com", username="test3", password="aaAA11!!", full_name="test user"
        )

        user2 = User.objects.create_user(
            email="test2@test.com", username="test2", password="aaAA11!!", full_name="test user"
        )

        user3 = User.objects.create_user(
            email="test4@test.com", username="test4", password="aaAA11!!", full_name="test user"
        )

        response = self.client.get(url)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res_json, list)
        self.assertEqual(len(res_json), 3)
        self.assertNotEqual(res_json[0], res_json[1] or res_json[2])
        self.assertNotEqual(res_json[1], res_json[2] or res_json[0])
        self.assertEqual(res_json[0]['email'], user1.email)
        self.assertEqual(res_json[1]['email'], user2.email)
        self.assertEqual(res_json[2]['email'], user3.email)
        self.assertEqual(res_json[0]['username'], user1.username)
        self.assertEqual(res_json[1]['username'], user2.username)
        self.assertEqual(res_json[2]['username'], user3.username)
        self.assertEqual(res_json[0]['full_name'], user1.full_name)
        self.assertEqual(res_json[1]['full_name'], user2.full_name)
        self.assertEqual(res_json[2]['full_name'], user3.full_name)
        self.assertNotIn('password', res_json[0] or res_json[1] or res_json[2])
        self.assertIn('id', res_json[0] and res_json[1] and res_json[2])
