# Std. Libs
import json
# Django Libs
from django.shortcuts import render
from rest_framework.serializers import Serializer
from django.contrib.auth.models import AnonymousUser

# Other frameworks Libs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Local packages
from .models import Project, Issue, Comment, Contributor


class ProjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        list_projects = Project.objects.all()
        serialized_list = Serializer(data=list_projects)
        if serialized_list.is_valid():
            content = serialized_list.data
        else:
            content = {"Error": "List not valid."}
            return Response(content)
        return Response(content.data)

class ProjectCreation(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = json.loads(request.body)

        if content:
            stitle = content["title"]
            sdescription = content["description"]
            stype = content["type"]
            suser = request.user
            
            project = Project(title=stitle, description=sdescription, type=stype, author_user_id=suser)
            print("SAVING")
            project.save()
            print("SAVED!")
            return Response(content)
        return Response({"Error": "not valid"})
