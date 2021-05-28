# Django Libs
from django.contrib.auth.models import User
from django.db.models import Q

# Other frameworks Libs
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Local packages
from .models import (Project,
                     Contributor,)
from .permissions import (ContributorPermissions,)
from .serializers import (ContributorSerializer,)


class UserTHROUGH(viewsets.ViewSet):
    """Contributor management

    Bridge between models : Project | User

        model table : through

    Generic arguments:
        - id (int) : ID of the project
        - pk (int) : ID of the contributor

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

    Generic Error:
        (HTTP status_code | detail)
        - 401 : jwt_access_token time over
    """
    permission_classes = (ContributorPermissions,)

    def list(self, request, id):
        """
        GET request
        Method list

        List all contributor for the project.
        Need to be one of them to get the list.

        Validate :
            (HTTP status_code | detail)
            - 200 : contributors' list
        Errors :
            (HTTP status_code | detail)
            - 400 : Element doesn't exist
            - 403 : Not permission to list
            - 404 : Error no contributor found
        """
        # Check if contributor
        try:
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
        # Should always get one contributor : the author.
        try:
            contributors = Contributor.objects.filter(project_id=id)
        except Exception:
            content = {"detail": "No contributor for project {id}."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        serialized_contributors = ContributorSerializer(contributors,
                                                        many=True)
        return Response(data=serialized_contributors.data,
                        status=status.HTTP_200_OK)

    def create(self, request, id):
        """
        POST request
        Method create

        Add a contributor to the project that user own.
        Need to be the author to add a contributor.

        Form:
            - user_id
            - role

        Validate :
            (HTTP status_code | detail)
            - 201 : contributor created
            - 208 : Already a contributor
        Errors :
            (HTTP status_code | detail)
            - 400 : Element doesn't exist
            - 403 : Not permission to create
        """
        # Check if creator is author
        try:
            contrib_creator = Contributor.objects.get(Q(project_id=id) &
                                                      Q(permission='1'))
            if contrib_creator.user_id.id != request.user.id:
                content = {"detail": "You're not the author."
                                     "You cannot add contributors."}
                return Response(data=content,
                                status=status.HTTP_403_FORBIDDEN)
        except Contributor.DoesNotExist:
            pass

        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Form is invalid."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        if content:
            try:
                if Contributor.objects.get(Q(project_id=id) &
                                           Q(user_id=content["user_id"])):
                    content = {"detail": "User is already a "
                               "contributor for the project {id}."}
                    return Response(data=content,
                                    status=status.HTTP_208_ALREADY_REPORTED)
            except Contributor.DoesNotExist:
                # User is not already a contributor
                pass
            try:
                content["user_id"] = User.objects.get(id=content['user_id'])
                content["project_id"] = Project.objects.get(id=id)
                # To secure and set one and only author.
                content["permission"] = "0"
                contributor = Contributor(**content)
            except ValueError:
                content = {"detail": "User doesn't exist."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                content = {"detail": "User doesn't exist."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                content = {"detail": "You do not have permission "
                                     "to add contributors."}
                return Response(data=content,
                                status=status.HTTP_403_FORBIDDEN)
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

        Validate :
            (HTTP status_code | detail)
            - 200 : deleted confirmation
                    project_id
                    user_id
        Errors :
            (HTTP status_code | detail)
            - 400 : Element doesn't exist
            - 401 : Unauthorize to delete an author
            - 403 : Not permission to delete
        """
        # Check if author try to delete him self from contrib's list.
        if pk == request.user.id:
            content = {"detail": "You cannot delete yourself from"
                                 "the contributor list."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)
        # Check if project exists
        try:
            # Check if user has right to destroy a contributor.
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if the delete request really concern a project's contributor.
        try:
            contributor = Contributor.objects.get(Q(user_id=pk) &
                                                  Q(project_id=id))
        except Exception:
            content = {"detail": f"User {pk} is not a contributor "
                                 f"for projet {id}."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if the user targetted has same right that the author.
        serialized_contributor = ContributorSerializer(contributor)
        if serialized_contributor.data["permission"] == "1":
            content = {"detail": "You cannot delete a contributor "
                                 "that own it."}
            return Response(data=content,
                            status=status.HTTP_401_UNAUTHORIZED)
        # Check if user has permission to delete contributor.
        self.check_object_permissions(request, contributor)
        # Delete process.
        contributor.delete()
        content = {"detail": f"Contributor {pk} deleted from project {id}.",
                   "project_id": id,
                   "user_id": pk, }
        return Response(data=content,
                        status=status.HTTP_200_OK)
