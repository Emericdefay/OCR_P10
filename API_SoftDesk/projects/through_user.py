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
from .permissions import (ContributorPermissions,)
from .serializers import (ContributorSerializer,)


class UserTHROUGH(viewsets.ViewSet):
    """Contributor management

    Bridge between models : Project | User
        
        model table : through

    Methods:
        - GET    : list
        - POST   : create
        - DELETE : delete

    Permissions:
        Contributor : (Project | User)
            - list
        Owner : (Project | User)
            - list
            - create
            - destroy
    """
    permission_classes = (ContributorPermissions,)


    def list(self, request, id):
        """
        GET request
        Method list
        """
        try:
            contributors = Contributor.objects.filter(project_id=id)
        except Exception:
            content = {"detail": "No contributor for project {id}"}
            return Response(data=content,
                            status=status.HTTP_204_NO_CONTENT)
        serialized_contributors = ContributorSerializer(contributors, many=True)
        return Response(data=serialized_contributors.data,
                        status=status.HTTP_200_OK)

    def create(self, request, id):
        """
        POST request
        Method create

        Add a contributor to the project that user own.
        """
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Form is invalid."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        if content:
            if Contributor.objects.get(Q(project_id=id) & Q(user_id=content["user_id"])):
                content = {"detail": f"User {content['user_id']} is \
                            already a contributor for the project {id}"}
                return Response(data=content,
                                status=status.HTTP_208_ALREADY_REPORTED)
            try:
                contributor = Contributor(project_id=id, **content)
            except Exception:
                content = {"detail": "Form is invalid."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            contributor.save()
            serialized_contributor = ContributorSerializer(contributor)
            return Response(data=serialized_contributor.data,
                            status=status.HTTP_201_CREATED)
        else:
            content = {"detail": "Form is empty"}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id, pk):
        """
        DELETE request
        Method destroy

        Need to own the project to delete contibutors. 
        Cannot delete the owner from contributors
        """
        try:
            project = Project.objects.get(id=id)
        except Exception:
            content = {"detail": "Project {id} does not exist \
                        or you don't have the right to manipulate it."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)
        try:
            contributor = Contributor.objects.get(Q(user_id=pk) & Q(project_id=id))
        except Exception:
            content = {"detail": f"User {pk} is not a contributor for projet {id}."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

        if contributor["permission"] == 1:
            content = {"detail": "You cannot be deleted from contributors. \
                        You own it."}
            return Response(data=content,
                            status=status.HTTP_401_UNAUTHORIZED)
                            
        # Check if user has permission to delete contributor.
        self.check_object_permissions(request, contributor)
        contributor.delete()
        content = {"detail": f"Contributor {pk} deleted from project {id}.",
                   "project_id": id,
                   "user_id": pk,}
        return Response(data=content,
                        status=status.HTTP_200_OK)

