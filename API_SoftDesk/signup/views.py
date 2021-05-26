# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Signup(APIView):
    """Signup management"""
    def post(self, request):
        """
        POST request
        method post

        No permission required to create an user.

        Form :
            - username
            - first_name
            - last_name
            - email
            - password

        Validate :
            (HTTP status_code | detail)
            - 200 : user created
        Errors :
            (HTTP status_code | detail)
            - 400 : Invalid form
        """

        content = request.data
        # Check if data is not empty
        if content:
            try:
                data = dict()
                data["username"] = content["username"]
                data["first_name"] = content["first_name"]
                data["last_name"] = content["last_name"]
                data["email"] = content["email"]
                data["password"] = content["password"]
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.create_user(**data)
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            user.save()
            content = {"detail": "User created"}
            return Response(data=content,
                            status=status.HTTP_200_OK)
        else:
            content = {"detail": "Request content is empty"}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
