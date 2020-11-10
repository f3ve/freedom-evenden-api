from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.user.views import UsersView

urlpatterns = [path("users/", UsersView.as_view(), name="users")]
