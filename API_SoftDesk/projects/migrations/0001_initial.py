# Generated by Django 3.2.3 on 2021-05-19 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=511)),
                ('description', models.CharField(max_length=8191)),
                ('type', models.CharField(max_length=63)),
                ('author_user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=511)),
                ('desc', models.CharField(max_length=4095)),
                ('tag', models.CharField(max_length=127)),
                ('priority', models.CharField(max_length=63)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assignee_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_related', to=settings.AUTH_USER_MODEL)),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('0', False), ('1', True)], max_length=15)),
                ('role', models.CharField(max_length=255)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=4095)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('issue_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.issue')),
            ],
        ),
    ]
