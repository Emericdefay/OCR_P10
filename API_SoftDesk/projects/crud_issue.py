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
from .permissions import (ProjectPermissions,
                          ContributorPermissions,
                          IssuePermissions,
                          CommentPermissions,)
from .serializers import (ProjectSerializer,
                          ContributorSerializer,
                          IssueSerializer,
                          CommentSerializer)


class IssueCRUD(viewsets.ViewSet):
    """Issue management

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
    """
    permission_classes = (IssuePermissions,)

    def list(self, request, id):
        """
        GET request
        Method list

        List all issues from a project if user is a contributor
        """
        # Check if user is contributor
        Project.objects.get(id=id)
        # List issues
        issues = Issue.objects.filter(project_id=id)
        serialized_issues = IssueSerializer(issues, many=True)
        return Response(serialized_issues.data)

    def create(self, request, id):
        """
        POST request
        """
        content = dict(request.data.items())
        if content:
            # Issue creation
            data = dict()
            data["title"] = content["title"]
            data["desc"] = content["desc"]
            data["tag"] = content["tag"]
            data["priority"] = content["priority"]
            data["project_id"] = Project.objects.get(id=id)
            data["status"] = content["status"]
            data["author_user_id"] = User.objects.get(id=request.user.id)
            data["assignee_user_id"] = User.objects.get(id=content["assignee_user_id"])
            # 'created_time' is automatically implemented

            issue = Issue(**data)
            issue.save()

            return Response({"Success": f"Created Issue {issue} successfully for project {id}"})
        return Response({"detail": f"Couldn't create Issue for Project {id}"})

    def update(self, request, id, pk):
        """
        PUT request
        """
        # Check permissions issue
        issue = Issue.objects.get(id=pk)
        self.check_object_permissions(request, issue)

        # form data
        content = dict(request.data.items())

        if content:
            issue = Issue.objects.filter(id=pk).update(**content)
            return Response(content)
        return Response({"detail": f"Couldn't update issue {pk} for project{id}"})


    def destroy(self, request, id, pk):
        """
        DELETE request
        """
        # Check permissions issue
        issue = Issue.objects.get(Q(id=pk) & Q(project_id=Project.objects.get(id=id)))
        self.check_object_permissions(request, issue)

        try:
            # issue.delete() Disable for developement

            return Response({"Success": f"Successfully delete issue {pk} from project {id}"})
        except Exception as e:
            return Response({f"detail - {e}": f"Delete not applied."})
