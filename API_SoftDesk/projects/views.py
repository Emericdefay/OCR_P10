# Std. Libs
import json

# Django Libs
from django.contrib.auth.models import User
from django.db.models import Q

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
from .permissions import (ElementPermissions,
                          ProjectPermissions,
                          ContributorPermissions)
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
    permission_classes = (ProjectPermissions,)

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
        Method retrieve
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
        Method create

        Create a new projet. Need to be connected to create one.
        """
        content = dict(request.data.items())
        if content:
            # Creation of the projet
            suser = User.objects.get(username=request.user)
            project = Project(author_user_id=suser, **content)
            project.save()
            # Create a first "contributor": author
            #id_project = project.id
            contributor = Contributor(permission="1", role="author", project_id=project, user_id=suser)
            contributor.save()

            return Response(content)
        return Response({"Error": "not valid"})

    def update(self, request, pk):
        """
        PUT request
        Method update

        Need to own the project to update it.
        """
        print("method : update")
        project_updated = Project.objects.get(id=pk)
        self.check_object_permissions(request, project_updated)
        project = Project.objects.filter(id=pk)
        content = dict(request.data.items())
        if content:
            project.update(**content)
            return Response(content)
        return Response({"Error": "Couldn't update"})

    def destroy(self, request, pk):
        """
        DELETE request
        """
        project_deleted = Project.objects.get(id=pk)
        self.check_object_permissions(request, project_deleted)
        #project_deleted.delete() # Comments for developpement
        return Response({"Success": f"Delete project {pk}"})


class UserCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (ContributorPermissions,)

    def list(self, request, id):
        """
        GET request
        Method list
        """
        contributors = Contributor.objects.filter(project_id=id)
        print(contributors)
        #self.check_object_permissions(request, contributors)
        serialized_contributors = ContributorSerializer(contributors, many=True)
        return Response(serialized_contributors.data)

    def create(self, request, id):
        """
        POST request
        """
        content = dict(request.data.items())
        print(f"content USER : {content}")
        if content:
            contributor = Contributor(project_id=id, **content)
            self.check_object_permissions(request, contributor) # Contributors' permissions
            contributor.save()
            return Response(content)
        return Response({"Error": "not valid"})

    def destroy(self, request, id, pk):
        """
        GET request
        """
        try:
            project = Project.objects.get(id=id)
            print(f" project : {project}")
            contributor = Contributor.objects.get(Q(user_id=pk) & Q(project_id=id))
            serial = ContributorSerializer(contributor)
            print(f"contributor : {serial.data}")
        except Exception as e:
            return Response({f"Error - {e}": f"Couldn't delete {pk} from project {id}"})
        self.check_object_permissions(request, contributor)
        #contributor.delete() # Avoid from developpement
        return Response({"Success": f"Delete Contributor {pk} from project {id}"})


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
