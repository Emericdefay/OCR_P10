# Local packages
from .crud_project import ProjectCRUD
from .through_user import UserTHROUGH
from .crud_issue import IssueCRUD
from .crud_comment import CommentCRUD


class ProjectView(ProjectCRUD):
    """Projects management

    Generic argument:
        - pk (int) : ID of the project

    Methods:
        - GET    : list
        - GET    : retrieve
        - POST   : create
        - PUT    : update
        - DELETE : delete

    Permissions:
        AUTHENTICATED :
            - create
        Contributor :
            - list
            - retrieve
        Owner :
            - list
            - retrieve
            - update
            - destroy
    """
    pass


class UserView(UserTHROUGH):
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
    """
    pass


class IssueView(IssueCRUD):
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
    """
    pass


class CommentView(CommentCRUD):
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
    pass
