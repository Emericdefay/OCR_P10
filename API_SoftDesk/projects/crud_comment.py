# Django Libs
from django.contrib.auth.models import User
# from django.db.models import Q

# Other frameworks Libs
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Local packages
from .models import (Project,
                     Issue,
                     Comment,)
from .permissions import (CommentPermissions,)
from .serializers import (CommentSerializer)


class CommentCRUD(viewsets.ViewSet):
    """Comment management

    Generic arguments:
        - id (int)       : ID of the project
        - issue_id (int) : ID of the issue
        - pk (int)       : ID of the comment

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
        Method list

        Need to be a contributor to list comments.

        Validate :
            (HTTP status_code | detail)
            - 200 : comments' list
            - 204 : No comment
        Errors : 
            (HTTP status_code | detail)
            - 400 : Element doesn't exist | Invalid form
            - 403 : Not permission to list
        """
        # Check if project exist
        try:
            # Check if user is contributor
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if issue exists
        try:
            Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            content = {"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.filter(issue_id=issue_id)
        serialized_comment = CommentSerializer(comment, many=True)
        # Check if comments exist
        if comment:
            return Response(data=serialized_comment.data,
                                status=status.HTTP_200_OK)
        else:
            # Return an empty json : []
            return Response(data=serialized_comment.data,
                            status=status.HTTP_204_NO_CONTENT)

    def create(self, request, id, issue_id):
        """
        POST request
        Method create

        Need to be a contributor to the project
        to create a comment on a existing issue.

        Form :
            - description

        Validate :
            (HTTP status_code | detail)
            - 201 : created comment
        Errors : 
            (HTTP status_code | detail)
            - 400 : Element doesn't exist | Invalid form
            - 403 : Not permission to create
        """
        # Check if project exist
        try:
            # Check if contributor to project
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if issue exist
        try:
            Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            content = {"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if content is valid
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
                data = dict()
                data["description"] = content["description"]
                user_id = User.objects.get(id=request.user.id)
                data["author_user_id"] = user_id
                data["issue_id"] = Issue.objects.get(id=issue_id)
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if content is conform
            try:
                comment = Comment(**data)
            except Exception:
                content = {"detail": "Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            comment.save()

            serialized_comment = CommentSerializer(comment)
            return Response(data=serialized_comment.data,
                            status=status.HTTP_201_CREATED)
        else:
            content = {"detail": "Form is empty."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id, issue_id, pk):
        """
        GET request
        Method retrieve

        Need to be a contributor to get a comment.

        Validate :
            (HTTP status_code | detail)
            - 200 : data retrieve
        Errors : 
            (HTTP status_code | detail)
            - 400 : Element doesn't exist
            - 403 : Not permission to retrieve
        """
        # Project exist
        try:
            # is contributor to project
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)        
        # issue exist
        try:
            Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            content = {"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # get comment if exist
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            content = {"detail": "Comment doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            content = {"detail": f"Couldn't get the comment {pk}."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)
        # Check if user has right to retrieve this comment.    
        self.check_object_permissions(request, comment)

        serialized_comment = CommentSerializer(comment)
        return Response(data=serialized_comment.data,
                        status=status.HTTP_200_OK)

    def update(self, request, id, issue_id, pk):
        """
        PUT request
        Method update

        Need to own the comment to update it.

        Form :
            - description

        Validate :
            (HTTP status_code | detail)
            - 200 : data updated
        Errors : 
            (HTTP status_code | detail)
            - 400 : Element doesn't exist | invalid form
            - 403 : Not permission to update
        """
        try:
            # is contributor to project
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content = {"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # issue exist
            Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            content = {"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # get comment if exist
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            content = {"detail": "Comment doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)           
        except Exception:
            content = {"detail":"Cannot access this comment."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)
        # Check if user has permission to update it
        self.check_object_permissions(request, comment)
        # Check if content is valid
        try:
            content = dict(request.data.items())
        except Exception:
            content = {"detail": "Invalid form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if content is not empty
        if content:
            # Check if comment exist
            try:
                comment = Comment.objects.filter(id=pk)
            except Exception:
                content = {"detail": "Comment does not exist."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if form is valid
            try:
                comment.update(content["description"])
            except Exception:
                content = {"detail": f"Invalid form."}
                return Response(data=content,
                                status=status.HTTP_400_BAD_REQUEST)

            serialized_comment = CommentSerializer(comment, many=True)
            return Response(data=serialized_comment.data,
                            status=status.HTTP_200_OK)
        else:
            content = {"detail": "Empty form."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id, issue_id, pk):
        """
        DELETE request
        Method destroy

        Need to own the comment to destroy it.

        Validate :
            (HTTP status_code | detail)
            - 200 : Successfully delete comment
                    project_id
                    issue_id
                    comment_id
        Errors : 
            (HTTP status_code | detail)
            - 400 : Element doesn't exist
            - 403 : Not permission to delete
        """
        # Check if project exists
        try:
            # is contributor to project
            Project.objects.get(id=id)
        except Project.DoesNotExist:
            content={"detail": "Project doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # issue exist
            Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            content={"detail": "Issue doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        # get comment if exist
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            content={"detail": "Comment doesn't exist."}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            content = {"detail": "You don't have permission to " \
                                 "delete this comment."}
            return Response(data=content,
                            status=status.HTTP_403_FORBIDDEN)
        self.check_object_permissions(request, comment)
        # Delete process
        comment.delete()
        content = {"detail": f"Successfully delete comment {pk}.",
                   "project_id": id,
                   "issue_id": issue_id,
                   "comment_id": pk}
        return Response(data=content,
                        status=status.HTTP_200_OK)

