# Django Libs
# from django.urls import path

# Django REST Libs
from rest_framework.routers import (SimpleRouter,)

# Local Libs
from . import views


#app_name = ""

router = SimpleRouter()
router.register(r"",
                views.ProjectView,
                basename="projects")
router.register(r"^(?P<id>[^/.]+)/users",
                views.UserView,
                basename="users")
router.register(r"^(?P<id>[^/.]+)/issues",
                views.IssueView,
                basename="issues")
router.register(r"^(?P<id>[^/.]+)/issues/(?P<issue_id>[^/.]+)/comments",
                views.CommentView,
                basename="comments")

urlpatterns = router.urls
