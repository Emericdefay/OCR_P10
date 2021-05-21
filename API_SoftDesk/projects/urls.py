# Django Libs
from django.urls import path

# Local Libs
from . import views


#app_name = ""

urlpatterns = [
    #path("", views.ProjectCRUD.as_view()),
    path(
    "<int:id>/",
    views.ProjectCRUD.as_view(),
    name="project-crud"
        ),
    path(
    "<int:id>/users/<int:user_id>/",
    views.UserCRUD.as_view(),
    name="user-crud"
        ),
    path(
    "<int:id>/issues/<int:issue_id>/",
    views.IssueCRUD.as_view(),
    name="issue-crud"
        ),
    path(
    "<int:id>/issues/<int:issue_id>/commments/<int:comment_id>/",
    views.CommentCRUD.as_view(),
    name="comment-crud"
        ),
]
