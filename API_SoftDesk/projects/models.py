from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=511)
    description = models.CharField(max_length=8191)
    type = models.CharField(max_length=63)
    author_user_id = models.ForeignKey(User, on_delete=CASCADE, default=None)


class Issue(models.Model):
    title = models.CharField(max_length=511)
    desc = models.CharField(max_length=4095)
    tag = models.CharField(max_length=127)
    priority = models.CharField(max_length=63)
    author_user_id = models.ForeignKey(User, on_delete=CASCADE)
    assignee_user_id = models.ForeignKey(User,related_name="contributor_related", on_delete=CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    #comment_id = models.IntegerField()
    description = models.CharField(max_length=4095)
    author_user_id = models.ForeignKey(User, on_delete=CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    project_id = models.ForeignKey(Project, on_delete=CASCADE)
    PERMISSIONS =[("0", False),
                  ("1", True)]
    permission = models.CharField(max_length=15, choices=PERMISSIONS)
    role = models.CharField(max_length=255)