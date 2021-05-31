# Django REST Libs
from rest_framework import permissions
# Local Libs
from .models import Contributor, Project


class ProjectPermissions(permissions.BasePermission):
    """Projects permissions

        User permissions :
            - list
            - create
            - retrieve
            - update
            - destroy

        Object manipulation permissions :
            - retrieve
            - update
            - destroy
    """
    def has_permission(self, request, view):
        """
        User should list, create, retrieve, update and destroy
        there own elements if user_connected.
        """
        if view.action in ["list", "create", "retrieve", "update", "destroy"]:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Object manipulation.

        Can retrieve object only if user is contributor
        Can update/destroy object only if user if author
        """
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # -> user_connected
        if view.action == 'retrieve':
            # User can retrieve element if user_is_contributor
            contributors = Contributor.objects.values()
            project = Project.objects.filter(id=obj.id)
            project_contributors = contributors.filter(
                project_id_id__in=project.values_list(
                    "id")).values_list("user_id")
            for contrib in list(project_contributors):
                if request.user.id in contrib:
                    return True
            return False
        elif view.action in ["update", "destroy"]:
            # User can update and destroy element if user_created_it
            return obj.author_user_id == request.user
        else:
            return False


class ContributorPermissions(permissions.BasePermission):
    """Projects permissions

        User permissions :
            - list
            - create
            - destroy

        Object manipulation permissions :
            - destroy
    """
    def has_permission(self, request, view):
        """
        User should list, create and destroy
        there own elements if user_connected.
        """
        if not request.user.is_authenticated:
            return False
        if view.action == 'list':
            # User should see all elements if user_connected
            return request.user.is_authenticated
        elif view.action in ["create", "destroy"]:
            # author should create there own contributors
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Object manipulation.

        Can destroy object only if user if author
        """
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # user_connected
        elif view.action == "destroy":
            # User can destroy element is user_created_it
            project = Project.objects.get(id=obj.project_id.id)
            return project in Project.objects.filter(
                                            author_user_id=request.user.id)
        else:
            return False


class IssuePermissions(permissions.BasePermission):
    """Projects permissions

        User permissions :
            - list
            - create
            - update
            - destroy

        Object manipulation permissions :
            - update
            - destroy
    """
    def has_permission(self, request, view):
        """
        User should list, create, retrieve, update and destroy
        there own elements if user_connected.
        """
        if view.action == 'list':
            # User should see all elements if user_connected
            return request.user.is_authenticated
        elif view.action in ["create", "update", "destroy"]:
            # User should retrieve, update and destroy there own elements
            # if user_connected
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Object manipulation.

        Can retrieve object only if user is contributor
        Can update/destroy object only if user if author
        """
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        elif view.action in ["update", "destroy"]:
            # User can update, destroy element if user_created_it
            project = Project.objects.get(id=obj.project_id.id)
            return obj.author_user_id == request.user
        else:
            return False


class CommentPermissions(permissions.BasePermission):
    """Projects permissions

        User permissions :
            - list
            - create
            - retrieve
            - update
            - destroy

        Object manipulation permissions :
            - retrieve
            - update
            - destroy
    """
    def has_permission(self, request, view):
        """
        User should list, create, retrieve, update and destroy
        there own elements if user_connected.
        """
        if view.action == 'list':
            # User should see all elements if user_connected
            return request.user.is_authenticated
        elif view.action in ["create", "retrieve", "update", "destroy"]:
            # User should retrieve, update and destroy there own elements
            # if user_connected
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Object manipulation.

        Can retrieve object only if user is contributor
        Can update/destroy object only if user if author
        """
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # -> user_connected
        if view.action == 'retrieve':
            # User can get element if user_is_contributor
            contributors = Contributor.objects.values()
            project = Project.objects.filter(id=obj.id)
            project_contributors = contributors.filter(
                project_id_id__in=project.values_list(
                    "id")).values_list("user_id")
            for contrib in list(project_contributors):
                if request.user.id in contrib:
                    return True
            return False
        elif view.action in ["update", "destroy"]:
            # User can update element is user_created_it
            return obj.author_user_id == request.user
        else:
            return False
