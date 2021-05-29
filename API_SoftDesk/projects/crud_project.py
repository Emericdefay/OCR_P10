# Django Libs
from django.contrib.auth.models import User
# from django.db.models import Q

# Other frameworks Libs
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Local packages
from .models import (Project,
                     Contributor,)
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

    Generic Error:
        (HTTP status_code | detail)
        - 401 : JWT authentification failed
    """
    permission_classes = (ProjectPermissions,)

    def list(self, request):
        """
        GET request
        Method list

        Show all projects linked to the authenticated user

        Validate :
            (HTTP status_code | detail)
            - 200 : projects' list
            - 204 : No project
        Errors :
            (HTTP status_code | detail)
            - 403 : Not permission to list
        """
        # Show all projects
        projects = Project.objects.all()
        # Select them all if admin
        if request.user.is_superuser:
            serialized_list = ProjectSerializer(projects,
                                                many=True)
        # Select user's projects if not admin
        else:
            contrib_projects = projects.filter(
                id__in=Contributor.objects.filter(
                    user_id=request.user.id).values_list("project_id"))
            serialized_list = ProjectSerializer(contrib_projects,
                                                many=True)
        # Content available
        if serialized_list.data:
            content = serialized_list.data
            return Response(data=content,
                            status=status.HTTP_200_OK)
        # Content not available
        else:
            content = {"detail": "No project available."}
            return Response(data=content,
                            status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """
        GET request
        Method retrieve

        Get a specific project for the authenticated user.

        Validate :
            (HTTP status_code | detail)
            - 200 : retrieved project
        Errors :
            (HTTP status_code | detail)
            - 400 : Invalid form
            - 403 : Not permission to create
            - 404 : Element doesn't exist
        """
        # Get one project : id=pk
        try:
            project = Project.objects.get(id=pk)
        except Exception:
            content = {"detail": "Project doesn't exist."}
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
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST request
        Method create

        Create a new projet. Need to be connected to create one.

        Form:
            - title
            - description
            - type

        Validate :
            (HTTP status_code | detail)
            - 201 : created project
        Errors :
            (HTTP status_code | detail)
            - 400 : Invalid form
            - 403 : Not permission to create
            - 500 : Intern error
        """
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Form is invalid."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        if content:
            # Creation of the projet
            suser = User.objects.get(id=request.user.id)
            try:
                content["author_user_id"] = suser
                project = Project(**content)
            except Exception:
                content = {"detail": "Invalid keys in form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            # Saving process
            project.save()
            # Create the first "contributor": author
            try:
                contrib_attrib = dict()
                contrib_attrib["permission"] = "1"
                contrib_attrib["role"] = "author"
                contrib_attrib["project_id"] = project
                contrib_attrib["user_id"] = suser
                contributor = Contributor(**contrib_attrib)
            except Exception:
                content = {"detail": "Intern error"}
                return Response(data=content,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # Saving process
            contributor.save()

            serialized_project = ProjectSerializer(project)
            return Response(data=serialized_project.data,
                            status=status.HTTP_201_CREATED)
        else:
            content = {"detail": "Form is empty."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """
        PUT request
        Method update

        Need to own the project to update it.

        Form:
            - (title)
            - (description)
            - (type)

        Validate :
            (HTTP status_code | detail)
            - 200 : updated project
        Errors :
            (HTTP status_code | detail)
            - 400 : Invalid form
            - 403 : Not permission to update
            - 404 : Element doesn't exist
        """
        # Check if project exists
        try:
            # Check permission
            project_updated = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # check if user has permission to update this project
        self.check_object_permissions(request, project_updated)
        project = Project.objects.filter(id=pk)
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Form is invalid."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        if content:
            try:
                project.update(**content)
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            serialized_project = ProjectSerializer(project, many=True)
            return Response(data=serialized_project.data,
                            status=status.HTTP_200_OK)
        else:
            content = {"detail": "Empty form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """
        DELETE request
        Method destroy

        Need to own the project to delete it.

        Validate :
            (HTTP status_code | detail)
            - 200 : project deleted
                    project_id
        Errors :
            (HTTP status_code | detail)
            - 403 : Not permission to delete
            - 404 : Element doesn't exist
            - 417 : Expectation failed
        """
        # Check if project exists
        try:
            # Is contributor
            project_deleted = Project.objects.get(id=pk)
        except Exception:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check if user has permission to delete the project
        self.check_object_permissions(request, project_deleted)
        try:
            project_deleted.delete()
            content = {"detail": f"Project {pk} deleted.",
                       "project_id": pk}
            return Response(data=content,
                            status=status.HTTP_200_OK)
        except Exception:
            content = {"detail": "Could not delete the project."}
            return Response(data=content,
                            status=status.HTTP_417_EXPECTATION_FAILED)
