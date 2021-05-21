# Django Libs
from django.urls import path

# Local Libs
from . import views


urlpatterns = [
    path("signup/", views.Signin.as_view(), name="signup")
]
