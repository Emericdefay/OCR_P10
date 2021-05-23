# Django Libs
from django.urls import path

# Django REST Libs
from rest_framework.routers import (SimpleRouter,)
# Local Libs
from . import views

#app_name = ""

router = SimpleRouter()
router.register(r"", views.ProjectCRUD, basename="projects")
router.register(r"^(?P<id>[^/.])/users", views.UserCRUD, basename="users")
router.register(r"^(?P<id>[^/.])/issues", views.IssueCRUD, basename="issues")
router.register(r"^(?P<id>[^/.])/issues/^(?P<issue_id>[^/.])/comments", views.CommentCRUD, basename="comments")
print("------------------URLS--------------")
for url in router.urls:
    print(f"url : {url}")
#router.register(r"projects", views.UserCRUD, basename="users")

urlpatterns = router.urls

# urlpatterns = [
#     path("", views.ProjectCRUD.as_view()),
#     path(
#     "<int:id>/",
#     views.ProjectCRUD.as_view(),
#     name="project-crud"
#         ),
#     path(
#     "<int:id>/users/<int:user_id>/",
#     views.UserCRUD.as_view(),
#     name="user-crud"
#         ),
#     path(
#     "<int:id>/issues/<int:issue_id>/",
#     views.IssueCRUD.as_view(),
#     name="issue-crud"
#         ),
#     path(
#     "<int:id>/issues/<int:issue_id>/commments/",
#     views.CommentCRUD.as_view(),
#     name="comment-crud"
#         ),
#     path(
#     "<int:id>/issues/<int:issue_id>/commments/<int:comment_id>/",
#     views.CommentCRUD.as_view(),
#     name="comment-crud"
#         ),
# ]


