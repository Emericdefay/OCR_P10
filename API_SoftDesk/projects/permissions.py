from rest_framework import permissions


class ProjectPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            # User should see all projects if user_admin_connected
            return request.user.is_admin
        elif view.action == "create":
            # User should create project if user_connected
            return request.user.is_authenticated
        elif view.action in ["retrieve", "update", "partial_update", "destroy"]:
            # User should retrieve, update, partial_update and destroy there own projects if user_connected
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # -> user_connected
        if view.action == 'retrieve':
            # User can get project if user_created_it_ or user_admin
            return obj == request.user or request.user.is_admin
        elif view.action in ["update", "partial_update"]:
            # User can update project is user_created_it or user_admin
            return obj == request.user or request.user.is_admin
        elif view.action == "destroy":
            # User can destroy project is user_created_it or user_admin
            return obj == request.user or request.user_is_admin
        else:
            return False


class IssuePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            # User should see all issues if user_admin_connected
            return request.user.is_admin
        elif view.action == "create":
            # User should create issue if user_connected
            return request.user.is_authenticated
        elif view.action in ["retrieve", "update", "partial_update", "destroy"]:
            # User should retrieve, update, partial_update and destroy there own issues if user_connected
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # -> user_connected
        if view.action == 'retrieve':
            # User can get issue if user_created_it_ or user_admin
            return obj == request.user or request.user.is_admin
        elif view.action in ["update", "partial_update"]:
            # User can update issue is user_created_it or user_admin
            return obj == request.user or request.user.is_admin
        elif view.action == "destroy":
            # User can destroy issue is user_created_it or user_admin
            return obj == request.user or request.user_is_admin
        else:
            return False


class CommentPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            # User should see all comments if user_admin_connected
            return request.user.is_admin
        elif view.action == "create":
            # User should create comment if user_connected
            return request.user.is_authenticated
        elif view.action in ["retrieve", "update", "partial_update", "destroy"]:
            # User should retrieve, update, partial_update and destroy there own comments if user_connected
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            # No permission if not user_connected
            return False
        # -> user_connected
        if view.action == 'retrieve':
            # User can get comment if user_created_it or user_admin
            return obj == request.user or request.user.is_admin
        elif view.action in ["update", "partial_update"]:
            # User can update comment is user_created_it or user_admin
            return obj == request.user or request.user.is_admin
        elif view.action == "destroy":
            # User can destroy comment is user_created_it or user_admin
            return obj == request.user or request.user_is_admin
        else:
            return False
