"""
custom urls
"""

from django.urls import path
from api.user import views as userViews

urlpatterns = [
    path("users/", userViews.UsersView.as_view(), name="users"),
    path("users/<pk>/", userViews.UserDetailView.as_view(), name="user")
]
