"""
custom urls
"""

from django.urls import path
from api.user import views as userViews
from api.article import views as articleViews
from api.category import views as categoryViews

urlpatterns = [
    path("users/", userViews.UsersView.as_view(), name="users"),
    path("users/<pk>/", userViews.UserDetailView.as_view(), name="user"),
    path("articles/", articleViews.ArticlesView.as_view(), name="articles"),
    path("articles/<pk>/", articleViews.ArticleDetailView.as_view(), name="article"),
    path("categories/", categoryViews.CategoryView.as_view(), name="categories")
]
