# Local packages
from .crud_project import ProjectCRUD
from .crud_user import UserCRUD
from .crud_issue import IssueCRUD
from .crud_comment import CommentCRUD


class ProjectView(ProjectCRUD):
    class Meta:
        pass


class UserView(UserCRUD):
    class Meta:
        pass


class IssueView(IssueCRUD):
    class Meta:
        pass


class CommentView(CommentCRUD):
    class Meta:
        pass

