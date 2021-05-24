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


class CommentCRUD(viewsets.ViewSet):
    """[summary]

    Methods:
        - GET    : list
        - GET    : retrieve
        - POST   : create
        - PUT    : update
        - DELETE : delete

    Permissions:
        Contributor :
            - list
            - retrieve
            - create
        Owner :
            - list
            - retrieve
            - create
            - update
            - destroy
    """
    permission_classes = (CommentPermissions,)

    def list(self, request, id, issue_id):
        """
        GET request
        """
        project = Project.objects.get(id=id)
        issue = Issue.objects.get(id=issue_id)
        comment = Comment.objects.filter(issue_id__in=issue_id)

        serialized_comment = CommentSerializer(comment, many=True)

        if serialized_comment:
            return Response(serialized_comment.data)

    def create(self, request, id, issue_id):
        """
        POST request
        """
        # is contributor to project
        project = Project.objects.get(id=id)
        # issue exist
        issue = Issue.objects.get(id=issue_id)
        content = dict(request.data.items())
        if content:
            data = dict()
            data["description"] = content["description"]
            data["author_user_id"] = User.objects.get(id=request.user.id)
            data["issue_id"] = Issue.objects.get(id=issue_id)
            comment = Comment(**data)
            comment.save()
            return Response({"Success":f"Comment {comment.id} successfully created"})
        else:
            return Response({"detail": f"Couldn't create comment for issue {issue_id} from project {id}"})

    def retrieve(self, request, id, issue_id, pk):
        """
        GET request
        """
        # is contributor to project
        project = Project.objects.get(id=id)
        # issue exist
        issue = Issue.objects.get(id=issue_id)
        # get comment if exist
        try:
            comment = Comment.objects.get(id=pk)
            self.check_object_permissions(request, comment)
            serialized_comment = CommentSerializer(comment)
            return Response(serialized_comment)
        except Exception as e:
            return Response({f"detail - {e}": f"Couldn't get the comment {pk} from issue {issue_id} project {id}"})

    def update(self, request, id, issue_id, pk):
        """
        PUT request
        """
        # is contributor to project
        project = Project.objects.get(id=id)
        # issue exist
        issue = Issue.objects.get(id=issue_id)
        # get comment if exist
        try:
            comment = Comment.objects.get(id=pk)
            self.check_object_permissions(request, comment)
            content = dict(request.data.items())
            Comment.objects.filter(id=pk).update(content["description"])
            return Response(content)
        except Exception as e:
            return Response({f"detail - {e}": f"Couldn't update comment {pk}"})

    def destroy(self, request, id, issue_id, pk):
        """
        DELETE request
        """
        # is contributor to project
        project = Project.objects.get(id=id)
        # issue exist
        issue = Issue.objects.get(id=issue_id)
        # get comment if exist
        comment = Comment.objects.get(id=pk)
        self.check_object_permissions(request, comment)
        #comment.delete() # Disable for devellopement
        return Response({"Success": f"Successfully delete comment {pk}"})

