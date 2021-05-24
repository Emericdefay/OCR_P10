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
                          UserSerializer,
                          ContributorSerializer,
                          IssueSerializer,
                          CommentSerializer)


class ProjectCRUD(viewsets.ViewSet):
    """Projects management

    Methods:
        - GET    : list
        - GET    : retrieve
        - POST   : create
        - PUT    : update
        - DELETE : delete

    Permissions:

    """
    permission_classes = (ProjectPermissions,)

    def list(self, request):
        """
        GET request
        Show all projects linked to the current user
        """
        print(f"method : list")
        print(f"id : {request.user.id}")
        # Show all projects
        projects = Project.objects.all()
        # Show all of them if admin
        if request.user.is_superuser:
            serialized_list = ProjectSerializer(projects,
                                                many=True)
        # Show user's projects if not admin
        else:
            own_projects = projects.filter(author_user_id=request.user.id)
            serialized_list = ProjectSerializer(own_projects,
                                                many=True)

        if serialized_list.data:
            content = serialized_list.data
            return Response(data=content,
                            status=status.is_success)
        else:
            content = {"detail": "No content available."}
            return Response(data=content,
                            status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """
        GET request with specific id
        Method retrieve
        """
        print(f"method : retrieve")
        # Show one project : id=pk
        
        project = Project.objects.get(id=pk)
        serialized_project = ProjectSerializer(project)
        if serialized_project.data:
            content = serialized_project.data
            self.check_object_permissions(request, project)
        else:
            content = {"Error": "Project not valid."}
        return Response(content)

    def create(self, request):
        """ 
        POST request 
        Method create

        Create a new projet. Need to be connected to create one.
        """
        content = dict(request.data.items())
        if content:
            # Creation of the projet
            suser = User.objects.get(username=request.user)
            project = Project(author_user_id=suser, **content)
            project.save()
            # Create a first "contributor": author
            #id_project = project.id
            contributor = Contributor(permission="1", role="author", project_id=project, user_id=suser)
            contributor.save()

            return Response(content)
        return Response({"Error": "not valid"})

    def update(self, request, pk):
        """
        PUT request
        Method update

        Need to own the project to update it.
        """
        print("method : update")
        project_updated = Project.objects.get(id=pk)
        self.check_object_permissions(request, project_updated)
        project = Project.objects.filter(id=pk)
        content = dict(request.data.items())
        if content:
            project.update(**content)
            return Response(content)
        return Response({"Error": "Couldn't update"})

    def destroy(self, request, pk):
        """
        DELETE request
        """
        project_deleted = Project.objects.get(id=pk)
        self.check_object_permissions(request, project_deleted)
        #project_deleted.delete() # Comments for developpement
        return Response({"Success": f"Delete project {pk}"})


class UserCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (ContributorPermissions,)

    def list(self, request, id):
        """
        GET request
        Method list
        """
        contributors = Contributor.objects.filter(project_id=id)
        serialized_contributors = ContributorSerializer(contributors, many=True)
        return Response(serialized_contributors.data)

    def create(self, request, id):
        """
        POST request
        """
        content = dict(request.data.items())
        print(f"content USER : {content}")
        if content:
            if Contributor.objects.get(Q(project_id=id) & Q(user_id=content["user_id"])):
                return Response({"Error":f"User {content['user_id']} is already a contributor for the project {id}"})
            contributor = Contributor(project_id=id, **content)
            self.check_object_permissions(request, contributor) # Contributors' permissions
            contributor.save()
            return Response(content)
        return Response({"Error": "not valid"})

    def destroy(self, request, id, pk):
        """
        GET request
        """
        try:
            project = Project.objects.get(id=id)
            print(f" project : {project}")
            contributor = Contributor.objects.get(Q(user_id=pk) & Q(project_id=id))
            serial = ContributorSerializer(contributor)
            print(f"contributor : {serial.data}")
        except Exception as e:
            return Response({f"Error - {e}": f"Couldn't delete {pk} from project {id}"})
        self.check_object_permissions(request, contributor)
        #contributor.delete() # Avoid from developpement
        return Response({"Success": f"Delete Contributor {pk} from project {id}"})


class IssueCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = (IssuePermissions,)

    def list(self, request, id):
        """
        GET request
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
        return Response({"Error": f"Couldn't create Issue for Project {id}"})

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
        return Response({"Error": f"Couldn't update issue {pk} for project{id}"})


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
            return Response({f"Error - {e}": f"Delete not applied."})

class CommentCRUD(viewsets.ViewSet):
    """[summary]

    Args:
        APIView ([type]): [description]
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
            return Response({"Error": f"Couldn't create comment for issue {issue_id} from project {id}"})

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
            return Response({f"Error - {e}": f"Couldn't get the comment {pk} from issue {issue_id} project {id}"})

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
            return Response({f"Error - {e}": f"Couldn't update comment {pk}"})

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

