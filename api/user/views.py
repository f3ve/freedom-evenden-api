from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.user import serializers
from api.user.models import User


class UsersView(APIView):
    """
    List users, create a new user.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.error, status.HTTP_400_BAD_REQUEST)
