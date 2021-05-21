# Std. Libs
import json

# Django Libs
from django.contrib.auth.models import User

# Other frameworks Libs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Local packages
from .models import (Project,
                     Issue,
                     Comment,
                     Contributor)
from .serializers import (ProjectSerializer,
                          UserSerializer,
                          ContributorSerializer,
                          IssueSerializer,
                          CommentSerializer)


class ProjectCRUD(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None):
        """
        GET request
        Show all projects links to the current user
        """
        if not id:
            # Show all projects
            list_projects = Project.objects.all()
            serialized_list = ProjectSerializer(list_projects, many=True)
            if serialized_list:
                content = serialized_list.data
            else:
                content = {"Error": "List not valid."}
            return Response(content)
        else:
            # Show one project : id=pk
            project = Project.objects.get(id=id)
            serialized_project = ProjectSerializer(project)
            if serialized_project.is_valid():
                content = serialized_project.data
            else:
                content = {"Error": "Project not valid."}
            return Response(content)

    def post(self, request):
        """ 
        POST request 
        Create a new projet
        """
        content = dict(request.data.items())
        if content:
            stitle = content["title"]
            sdescription = content["description"]
            stype = content["type"]
            suser = User.objects.get(username=request.user)
            
            project = Project(title=stitle, description=sdescription, type=stype, author_user_id=suser)
            project.save()
            return Response(content)
        return Response({"Error": "not valid"})

    def put(self, request, id):
        """
        PUT request
        """
        pass

    def delete(self, request, id):
        """
        DELETE request
        """
        pass


class UserCRUD(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        """
        GET request
        """
        pass
    def post(self, request, id):
        """
        POST request
        """
        pass
    def delete(self, request, id, user_id):
        """
        DELETE request
        """
        pass


class IssueCRUD(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        """
        GET request
        """
        pass
    def post(self, request, id):
        """
        POST request
        """
        pass
    def put(self, request, id, issue_id):
        """
        PUT request
        """
        pass
    def delete(self, request, id, issue_id):
        """
        DELETE request
        """
        pass


class CommentCRUD(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, id, issue_id, comment_id=None):
        """
        GET request
        """
        if not comment_id:
            pass
        else:
            pass
    def post(self, request, id, issue_id):
        """
        POST request
        """
        pass
    def put(self, request, id, issue_id, comment_id):
        """
        PUT request
        """
        pass
    def delete(self, request, id, issue_id, comment_id):
        """
        DELETE request
        """
        pass
