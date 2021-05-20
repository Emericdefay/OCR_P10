from django.urls import path
from . import views

#app_name = ""
urlpatterns = [
    path("", views.ProjectView.as_view()),
    path("create/", views.ProjectCreation.as_view())
]
