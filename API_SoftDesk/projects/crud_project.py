# Std. Libs
import json

# Django Libs
from django.contrib.auth.models import User
from django.db.models import Q

# Other frameworks Libs
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Local packages
from .models import (Project,
                     Contributor,
                     Issue,
                     Comment,)
from .permissions import (ProjectPermissions,)
from .serializers import (ProjectSerializer,)


class ProjectCRUD(viewsets.ViewSet):
    """Projects management

    Generic argument:
        - pk (int) : ID of the project

    Methods:
        - GET    : list
        - GET    : retrieve
        - POST   : create
        - PUT    : update
        - DELETE : delete

    Permissions:
        AUTHENTICATED :
            - create
        Contributor :
            - list
            - retrieve
        Owner :
            - list
            - retrieve
            - update
            - destroy
    """
    permission_classes = (ProjectPermissions,)

    def list(self, request):
        """
        GET request
        Method list

        Show all projects linked to the authenticated user
        """
        # Show all projects
        projects = Project.objects.all()
        # Select them all if admin
        if request.user.is_superuser:
            serialized_list = ProjectSerializer(projects,
                                                many=True)
        # Select user's projects if not admin
        else:
            own_projects = projects.filter(author_user_id=request.user.id)
            contrib_projects = projects.filter(id__in=Contributor.objects.filter(user_id=request.user.id).values_list("id"))
            print(f"list of projects linked : \n{contrib_projects}")
            serialized_list = ProjectSerializer(contrib_projects,
                                                many=True)
        # Content available
        if serialized_list.data:
            content = serialized_list.data
            return Response(data=content,
                            status=status.HTTP_200_OK)
        # Content not available
        else:
            content = {"detail": "No content available."}
            return Response(data=content,
                            status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """
        GET request
        Method retrieve

        Get a specific project for the authenticated user.
        """
        # Get one project : id=pk
        try:
            project = Project.objects.get(id=pk)
        except Exception:
            content = {"detail": "Project does not exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)

        serialized_project = ProjectSerializer(project)
        if serialized_project.data:
            content = serialized_project.data
            # Check is user has permission to access this project
            self.check_object_permissions(request, project)
            return Response(content,
                            status=status.HTTP_200_OK)
        else:
            content = {"detail": "Project details not available."}
            return Response(content,
                            status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ 
        POST request 
        Method create

        Create a new projet. Need to be connected to create one.
        """
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Form is invalid."}
            return Response(data=content,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if content:
            # Creation of the projet
            suser = User.objects.get(username=request.user)
            try:
                project = Project(author_user_id=suser, **content)
            except Exception:
                content = {"detail": "Invalid keys in form."}
                return Response(data=content,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            project.save()
            # Create the first "contributor": author
            contributor = Contributor(permission="1",
                                      role="author",
                                      project_id=project,
                                      user_id=suser)
            contributor.save()

            serialized_project = ProjectSerializer(project)
            
            return Response(data=serialized_project.data,
                            status=status.HTTP_201_CREATED)
        else:
            content = {"detail": "Form is empty."}
            return Response(data=content,
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, pk):
        """
        PUT request
        Method update

        Need to own the project to update it.
        """
        print("method : update")
        try:
            project_updated = Project.objects.get(id=pk)
        except Exception:
            content = {"detail":"Project not found."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # check if user has permission to update this project
        self.check_object_permissions(request, project_updated)
        project = Project.objects.filter(id=pk)
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail":"Form is invalid."}
            return Response(data=content,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if content:
            project.update(**content)
            serialized_project = ProjectSerializer(project, many=True)
            return Response(data=serialized_project.data,
                            status=status.HTTP_200_OK)
        else:
            content = {"detail": "PUT form is empty."}
            return Response(data=content,
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, pk):
        """
        DELETE request
        Method destroy

        Need to own the project to delete it.
        """
        try:
            project_deleted = Project.objects.get(id=pk)
        except Exception:
            content = {"detail": "Project does not exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check if user has permission to delete the project
        self.check_object_permissions(request, project_deleted)
        try:
            project_deleted.delete() # Comments for developpement
            content = {"detail": f"Project {pk} deleted.",
                       "project_id": pk,}
            return Response(data=content,
                            status=status.HTTP_204_NO_CONTENT)
        except Exception:
            content = {"detail": "Could not delete the project."}
            return Response(data=content,
                            status=status.HTTP_417_EXPECTATION_FAILED)
