# Generated by Django 3.2.3 on 2021-05-23 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_issue_projet_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='projet_id',
            new_name='project_id',
        ),
    ]
