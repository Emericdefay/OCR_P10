# Django Libs
from django.urls import path

# Local Libs
from . import views


urlpatterns = [
    path("", views.Signup.as_view(), name="signup")
]
