"""
functions and tools to keep tests DRY
"""

from api.models import User


def create_test_user(n):
    """
    Creates a test user in the database
    """

    return User.objects.create_user(
        email="test@test%s.com" % n, username="testuser%s" % n,
        full_name="test user %s" % n, password="aaAA11!!"
    )


# Test User dicts for different test cases
invalid_password_user = {
    "username": "invalidPass",
    "email": "invalidpass@test.com",
    "full_name": "invalid password",
    "password": "inv"
}

invalid_username_user = {
    "username": "us",
    "email": "invaliduse@test.com",
    "full_name": "invalid username",
    "password": "aaAA11!!"
}

invalid_email_user = {
    "username": "invalidEmail",
    "email": "inv",
    "full_name": "invalid email",
    "password": "aaAA11!!"
}

missing_fields_user = {
    "username": "",
    "email": "",
    "full_name": "",
    "password": ""
}

test_user1 = {
    "username": "testUser1",
    "email": "testuser1@test.com",
    "full_name": "test user 1",
    "password": "aaAA11!!"
}

test_user2 = {
    "username": "testUser2",
    "email": "testuser2@test.com",
    "full_name": "test user 2",
    "password": "aaAA11!!"
}

test_user3 = {
    "username": "testUser3",
    "email": "testuser3@test.com",
    "full_name": "test user",
    "password": "aaAA11!!"
}
