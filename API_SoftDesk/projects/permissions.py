from django.contrib.auth.models import User

from rest_framework import permissions

from .models import Contributor, Project
from .serializers import ContributorSerializer

class ElementPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            # User should see all elements if user_admin_connected
            print(f"req : {request.user}")
            print(f"view : {view.action}")
            return request.user.is_authenticated
        elif view.action in ["create", "retrieve", "update", "partial_update", "destroy"]:
            # User should retrieve, update, partial_update and destroy there own elements if user_connected
            return request.user.is_authenticated
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # -> user_connected
        if view.action == 'retrieve':
            # User can get element if user_is_contributor or user_admin
            print(f"user_id : {request.user.id}")
            contributors = Contributor.objects.values()
            project = Project.objects.filter(id=obj.id)
            project_contributors = contributors.filter(project_id_id__in=project.values_list("id")).values_list("user_id")
            print(f"contributor : {list(project_contributors)}")
            for contrib in list(project_contributors):
                print(f"{request.user.id in contrib}")
                if request.user.id in contrib:
                    return True
            print(f"contributor {request.user.id} in : {request.user.id in list(project_contributors)}")
            print(f"project id : {obj.id}")
            print(f"user is contributor : {True if project_contributors else False}")
            return False
        elif view.action in ["update", "partial_update"]:
            # User can update element is user_created_it or user_admin
            return obj.author_user_id == request.user or request.user.is_superuser
        elif view.action == "destroy":
            # User can destroy element is user_created_it or user_admin
            return obj.author_user_id == request.user or request.user.is_superuser
        else:
            return False

