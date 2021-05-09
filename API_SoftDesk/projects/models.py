from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField()
    description = models.CharField()
    type = models.CharField()
    author_user_id = (User)


class Issue(models.Model):
    title = models.CharField()
    desc = models.CharField()
    tag = models.CharField()
    priority = models.CharField()
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField()
    author_user_id = models.ForeignKey(User)
    issue_id = models.ForeignKey(Issue)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user_id = models.ForeignKey(User)
    project_id = models.ForeignKey(Project)
    permission = models.Choices()
    role = models.CharField()