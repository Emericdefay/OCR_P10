from django.urls import path

from . import views


urlpatterns = [
    path("", views.Signin.as_view())
]
