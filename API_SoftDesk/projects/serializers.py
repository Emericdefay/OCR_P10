# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework import serializers

# Local Libs
from .models import Project, Issue, Contributor, Comment


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer based on serializers.ModelSerializer
    """
    class Meta():
        model = Project
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Serializer based on serializers.ModelSerializer
    """
    class Meta():
        model = User
        fields = ("username", "first_name", "last_name", "email")


class IssueSerializer(serializers.ModelSerializer):
    """Serializer based on serializers.ModelSerializer
    """
    class Meta():
        model = Issue
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer based on serializers.ModelSerializer
    """
    class Meta():
        model = Contributor
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Serializer based on serializers.ModelSerializer
    """
    class Meta():
        model = Comment
        fields = "__all__"
