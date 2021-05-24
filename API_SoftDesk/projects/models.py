# Django Libs
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Project(models.Model):
    title = models.CharField(
        max_length=511,
        null=False,
        blank=False)
    description = models.CharField(
        max_length=8191,
        null=False,
        blank=False)
    type = models.CharField(
        max_length=63,
        null=False,
        blank=False)
    author_user_id = models.ForeignKey(
        User,
        on_delete=CASCADE,
        null=False,
        blank=False)


class Issue(models.Model):
    title = models.CharField(
        max_length=511,
        null=False,
        blank=False)
    desc = models.CharField(
        max_length=4095,
        null=True,
        blank=True)
    tag = models.CharField(
        max_length=127,
        null=False,
        blank=False)
    priority = models.CharField(
        max_length=63,
        null=False,
        blank=False)
    project_id = models.ForeignKey(
        Project,
        on_delete=CASCADE,
        null=False,
        blank=False
    )
    status = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    author_user_id = models.ForeignKey(
        User,
        on_delete=CASCADE,
        null=False,
        blank=False)
    assignee_user_id = models.ForeignKey(
        User,
        related_name="contributor_related",
        on_delete=CASCADE,
        null=False,
        blank=False)
    created_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False)


class Comment(models.Model):
    description = models.CharField(
        max_length=4095,
        null=False,
        blank=False)
    author_user_id = models.ForeignKey(
        User,
        on_delete=CASCADE,
        null=False,
        blank=False)
    issue_id = models.ForeignKey(
        Issue,
        on_delete=CASCADE,
        null=False,
        blank=False)
    created_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False)


class Contributor(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=CASCADE,
        null=False,
        blank=False)
    project_id = models.ForeignKey(
        Project,
        on_delete=CASCADE,
        null=False,
        blank=False)
    PERMISSIONS = [("0", False),
                   ("1", True)]
    permission = models.CharField(
        max_length=15,
        choices=PERMISSIONS,
        null=False,
        blank=False)
    role = models.CharField(
        max_length=255,
        null=False,
        blank=False)
