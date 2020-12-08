"""
functions and tools to keep tests DRY
"""

import datetime
from api.models import User, Article
from api.article import serializers as articleSerializers


def create_test_user(n):
    """
    Creates a test user in the database
    """

    return User.objects.create_user(
        email="test@test%s.com" % n, username="testuser%s" % n,
        full_name="test user %s" % n, password="aaAA11!!"
    )


def create_test_article(n, user, draft):
    """
    Creates a test article in the database
    """
    today = datetime.date.today()

    return Article.objects.create(
        title="test article %s" % n,
        content="test article %s content" % n,
        author=user,
        slug="test_article_%s" % n,
        draft=draft,
        publish_date=today
    )


def serializerArticle(article):
    """
    serializes a article
    """
    return articleSerializers.ArticleSerializer(article)


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


def test_article1(user_id):
    """
    Creates a dictionary that represents a test article
    """

    return {
        "title": "Test Article 1",
        "content": "This is a test article yaya!",
        "slug": "test_article_1_slug",
        "draft": False,
        "publish_date": datetime.date.today(),
        "author": int(user_id)
    }
