# Django Libs
from django.urls import path

# Local Libs
from . import views


urlpatterns = [
    path("", views.Signin.as_view(), name="signup")
]
