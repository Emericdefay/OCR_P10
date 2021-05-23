# Std. Libs
import json

# Django Libs
from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import get_object_or_404

# Other frameworks Libs
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action

# Local packages
from .models import (Project,
                     Issue,
                     Comment,
                     Contributor)
from .permissions import (ElementPermissions)
from .serializers import (ProjectSerializer,
                          UserSerializer,
                          ContributorSerializer,
                          IssueSerializer,
                          CommentSerializer)


class ProjectCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = (ElementPermissions,)

    def list(self, request):
        """
        GET request
        Show all projects links to the current user
        """
        print(f"method : list")
        print(f"id : {request.user.id}")
        # Show all projects
        list_all_projects = Project.objects.all()
        # Show all of them if admin
        if request.user.is_superuser:
            serialized_list = ProjectSerializer(list_all_projects, many=True)
        # Show user's projects if not admin
        else:
            projects_from_user = list_all_projects.filter(author_user_id=request.user.id)
            serialized_list = ProjectSerializer(projects_from_user, many=True)
        
        if serialized_list.data:
            content = serialized_list.data
        else:
            content = {"Error": "List not valid."}
        return Response(content)

    def retrieve(self, request, pk):
        """
        GET request with specific id
        """
        print(f"method : retrieve")
        # Show one project : id=pk
        
        project = Project.objects.get(id=pk)
        serialized_project = ProjectSerializer(project)
        if serialized_project.data:
            content = serialized_project.data
            self.check_object_permissions(request, project)
        else:
            content = {"Error": "Project not valid."}
        return Response(content)

    def create(self, request):
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

    def update(self, request, id):
        """
        PUT request
        """
        pass

    def partial_update(self, request, id):
        """
        PUT request
        """
        pass

    def destroy(self, request, id):
        """
        DELETE request
        """
        pass


class UserCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (ElementPermissions,)

    def list(self, request, id):
        """
        GET request
        """
        pass

    def create(self, request, id):
        """
        POST request
        """
        content = dict(request.data.items())
        print(f"content USER : {content}")
        if content:
            #spermission = content["permission"]
            srole = content["role"]
            sproject_id = Project.objects.get(id=content["project_id"])
            suser_id = User.objects.get(id=content["user_id"])
            
            contributor = Contributor(role=srole, project_id=sproject_id, user_id=suser_id)
            contributor.save()
            return Response(content)
        return Response({"Error": "not valid"})

    def retrieve(self, request, id, pk):
        """
        POST request
        """
        pass

    def update(self, request, id, pk):
        """
        POST request
        """
        pass

    def partial_update(self, request, id, pk):
        """
        POST request
        """
        pass

    def destroy(self, request, id, pk):
        """
        DELETE request
        """
        pass



class IssueCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (ElementPermissions,)

    def list(self, request, id):
        """
        GET request
        """
        pass

    def create(self, request, id):
        """
        POST request
        """
        pass

    def retrieve(self, request, id, pk):
        """
        POST request
        """
        pass

    def update(self, request, id, pk):
        """
        POST request
        """
        pass

    def partial_update(self, request, id, pk):
        """
        POST request
        """
        pass

    def destroy(self, request, id, pk):
        """
        DELETE request
        """
        pass

class CommentCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (ElementPermissions,)

    def list(self, request, id, issue_id):
        """
        GET request
        """
        pass

    def create(self, request, id, issue_id):
        """
        POST request
        """
        pass

    def retrieve(self, request, id, issue_id, pk):
        """
        POST request
        """
        pass

    def update(self, request, id, issue_id, pk):
        """
        POST request
        """
        pass

    def partial_update(self, request, id, issue_id, pk):
        """
        POST request
        """
        pass

    def destroy(self, request, id, issue_id, pk):
        """
        DELETE request
        """
        pass
