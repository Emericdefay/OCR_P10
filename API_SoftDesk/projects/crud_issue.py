# Django Libs
from django.contrib.auth.models import User
from django.db.models import Q

# Other frameworks Libs
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Local packages
from .models import (Contributor, Project,
                     Issue,)
from .permissions import (IssuePermissions,)
from .serializers import (IssueSerializer,)


class IssueCRUD(viewsets.ViewSet):
    """Issue management

    Generic arguments:
        - id (int) : ID of the project
        - pk (int) : ID of the issue

    Methods:
        - GET    : list
        - POST   : create
        - PUT    : update
        - DELETE : delete

    Permissions:
        Contributor :
            - list
            - create
        Owner :
            - list
            - create
            - update
            - destroy

    Generic Error:
        (HTTP status_code | detail)
        - 401 : JWT authentification failed
    """
    permission_classes = (IssuePermissions,)

    def list(self, request, id):
        """
        GET request
        Method list

        List all issues from a project if user is a contributor

        Validate :
            (HTTP status_code | detail)
            - 200 : issue's list
        Errors :
            (HTTP status_code | detail)
            - 403 : Not permission to list
            - 404 : Element doesn't exist
        """
        # Check if project exist
        try:
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check user is contributor
        try:
            Contributor.objects.get(Q(project_id=id) &
                                    Q(user_id=request.user.id))
        except Contributor.DoesNotExist:
            content = {"detail": "No contributor for the project."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)
        # List issues
        issues = Issue.objects.filter(project_id=id)
        serialized_issues = IssueSerializer(issues, many=True)
        return Response(data=serialized_issues.data,
                        status=status.HTTP_200_OK)

    def create(self, request, id):
        """
        POST request
        Method create

        Need to be a contributor of the project to create an issue.

        Form:
            - title
            - desc
            - tag
            - priority
            - status
            - assignee_user_id

        Validate :
            (HTTP status_code | detail)
            - 201 : created issue
        Errors :
            (HTTP status_code | detail)
            - 400 : Invalid form
            - 403 : Not permission to create
            - 404 : Element doesn't exist
        """
        # Check if project exist
        try:
            # Check if user is contributor
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)

        # Check user is contributor
        try:
            Contributor.objects.get(Q(project_id=id) &
                                    Q(user_id=request.user.id))
        except Contributor.DoesNotExist:
            content = {"detail": "No contributor for the project."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)

        # Check if form is valid
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Invalid form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        if content:
            # Issue creation
            try:
                data = dict()
                data["title"] = content["title"]
                data["desc"] = content["desc"]
                data["tag"] = content["tag"]
                data["priority"] = content["priority"]
                data["project_id"] = Project.objects.get(id=id)
                data["status"] = content["status"]
                auth_id = User.objects.get(id=request.user.id)
                # assignee:
                if "assignee_user_id" in content:
                    assignee_id = User.objects.get(
                                        id=content["assignee_user_id"])
                # if no assignee, set assignee_user_id = request.user.id
                else:
                    assignee_id = User.objects.get(id=request.user.id)
                data["author_user_id"] = auth_id
                data["assignee_user_id"] = assignee_id
                # 'created_time' is automatically implemented
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if data is valid
            try:
                issue = Issue(**data)
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            # Saving process
            issue.save()
            # Serialize issue
            serialized_issue = IssueSerializer(issue)
            return Response(data=serialized_issue.data,
                            status=status.HTTP_201_CREATED)
        else:
            content = {"detail": "Empty form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id, pk):
        """
        PUT request
        Method update

        Need to own the issue to update it.

        Form:
            - (title)
            - (desc)
            - (tag)
            - (priority)
            - (status)
            - (assignee_user_id)

        Validate :
            (HTTP status_code | detail)
            - 200 : updated issue
        Errors :
            (HTTP status_code | detail)
            - 400 : Invalid form
            - 403 : Not permission to update
            - 404 : Element doesn't exist
        """
        # Check if project exist
        try:
            # is contributor
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check if issue exist
        try:
            issue = Issue.objects.get(id=pk)
        except Issue.DoesNotExist:
            content = {"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check permissions issue
        self.check_object_permissions(request, issue)
        # Check if content is a valid form
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Invalid form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if content is not empty
        if content:
            # Check if content is valid
            try:
                Issue.objects.filter(id=pk).update(**content)
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            issue = Issue.objects.get(id=pk)
            serialized_issue = IssueSerializer(issue)
            return Response(data=serialized_issue.data,
                            status=status.HTTP_200_OK)
        else:
            content = {"detail": "Empty form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id, pk):
        """
        DELETE request
        Method destroy

        Need to own issue to delete it.

        Validate :
            (HTTP status_code | detail)
            - 200 : delete details
                    project_id
                    issue_id
        Errors :
            (HTTP status_code | detail)
            - 403 : Not permission to delete
            - 404 : Element doesn't exist
            - 500 : Delete failed
        """
        # Check if project exist
        try:
            # is contributor
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check if issue exist
        try:
            issue = Issue.objects.get(
                Q(id=pk) &
                Q(project_id=Project.objects.get(id=id)))
        except Issue.DoesNotExist:
            content = {"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_404_NOT_FOUND)
        # Check permissions issue
        self.check_object_permissions(request, issue)
        try:
            issue.delete()
            content = {"detail": f"Successfully delete issue {pk}.",
                       "project_id": id,
                       "issue_id": pk}
            return Response(data=content,
                            status=status.HTTP_200_OK)
        except Exception:
            content = {"detail": "Delete not applied."}
            return Response(data=content,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
