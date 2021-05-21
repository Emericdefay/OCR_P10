# Std Libs
import json

# Django Libs
from django.shortcuts import render
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class Signin(APIView):
    """"""
    def post(self, request):
        """"""
        content = request.data
        if content:
            susername = content["username"]
            sfirst_name = content["first_name"]
            slast_name = content["last_name"]
            semail = content["email"]
            spassword = content["password"]
            user = User.objects.create_user(username=susername,
                                            first_name=sfirst_name,
                                            last_name=slast_name,
                                            email=semail,
                                            password=spassword,
                                            )
            user.save()
            return Response({"Success": "User created"})
        return Response({"Error": "Request content not valid"})