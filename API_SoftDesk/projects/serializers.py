#Std Libs

# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework import serializers

# Local Libs
from .models import Project, Issue, Contributor, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta():
        model = Project
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = "__all__" # Not ALL at final


class IssueSerializer(serializers.ModelSerializer):
    class Meta():
        model = Issue
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    class Meta():
        model = Contributor
        fields = "__all__" # Not ALL at final


class CommentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Comment
        fields = "__all__"