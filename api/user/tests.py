"""
User tests
"""

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api import test_helpers


class UserListTestCase(APITestCase):
    """
    Test users POST and GET
    """
    users_url = reverse("users")
    client = APIClient()

    def test_post_user(self):
        """
        test user is created properly
        """
        user = test_helpers.test_user1
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
        user = test_helpers.missing_fields_user
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
        user1 = test_helpers.create_test_user(1)
        user2 = test_helpers.create_test_user(2)
        user3 = test_helpers.create_test_user(3)
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


class UserDetailTestCase(APITestCase):
    """
    Tests for UserDetialView
    """

    client = APIClient()

    def test_get_user_by_id(self):
        """
        Should return 200 and requested user
        """
        user = test_helpers.create_test_user(1)
        url = reverse("user", args=[user.id])
        response = self.client.get(url, pk=user.id)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json['email'], user.email)
        self.assertEqual(res_json['username'], user.username)
        self.assertEqual(res_json['full_name'], user.full_name)
        self.assertNotIn('password', res_json)
        self.assertIn('id', res_json)
        self.assertIsNotNone(res_json['id'])
        self.assertIsInstance(res_json['id'], int)

    def test_get_nonexisting_user(self):
        """
        Should return 404 if user does not exist
        """

        url = reverse("user", args=[1])
        response = self.client.get(url, pk=1)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res_json['message'], 'User does not exist')

    def test_delete_user(self):
        """
        Should return 204 and delete requested user
        """

        user = test_helpers.create_test_user(1)
        url = reverse("user", args=[user.id])
        del_res = self.client.delete(url, pk=user.id)
        get_res = self.client.get(url, pk=user.id)
        res_json = get_res.json()

        # Check delete response
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

        # Test that user has actually been deleted
        self.assertEqual(get_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res_json["message"], 'User does not exist')

    def test_delete_nonexisting_user(self):
        """
        Should return 404 and error message
        """
        url = reverse("user", args=[1])
        response = self.client.delete(url, pk=1)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res_json["message"], 'User does not exist')

    def test_patch_user(self):
        """
        Should return 203 and update the specified user
        """

        user = test_helpers.create_test_user(0)
        url = reverse("user", args=[user.id])
        updated_fields = {
            "username": "newUserName",
            "email": "newemail@new.com",
            "full_name": "new name",
            "password": "newPassword11!!"
        }
        response = self.client.patch(url, pk=user.id, data=updated_fields)
        res_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
