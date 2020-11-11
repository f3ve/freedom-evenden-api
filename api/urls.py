"""
custom urls
"""

from django.urls import path
from api.user.views import UsersView

urlpatterns = [
    path("users/", UsersView.as_view(), name="users"),
    # path("users/<pk>/", UserDetailView.as_View(), name="userDetail")
]
