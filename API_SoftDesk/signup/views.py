import json

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

class Signin(APIView):

    def post(self, request):
        print("-----------------------")
        content = request.data
        if content:
            susername = content["username"]
            sfirst_name = content["first_name"]
            slast_name = content["last_name"]
            semail = content["email"]
            spassword = content["password"]
            user = User(username=susername ,first_name=sfirst_name, last_name=slast_name, email=semail, password=spassword)
            user.save()
        return Response(content)