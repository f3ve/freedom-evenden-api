"""
User views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.user import serializers
from api.models import User


class UsersView(APIView):
    """
    List users, create a new user.
    """

    def get(self, request):
        """
        returns all users from database
        """
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new user in database
        """
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    GET, PATCH, DELETE specific user by id
    """

    def get_object(self, pk, call_back):
        """
        attempts to fetch user then calls the provided callback function, if
        user does not exist returns 404 with error message
        """
        try:
            user = User.objects.get(pk=pk)
            return call_back(user)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk):
        """
        get user by id
        """

        def return_user(user):
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)

        return self.get_object(pk, return_user)

    def patch(self, request, pk):
        """
        PATCH fields in specified user
        """

        def update_user(user):
            serializer = serializers.UserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return self.get_object(pk, update_user)

    def delete(self, request, pk):
        """
        deletes specified user
        """
        def delete_user(user):
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.get_object(pk, delete_user)
