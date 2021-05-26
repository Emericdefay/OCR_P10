# flake8: noqa
# Generated by Django 3.2.3 on 2021-05-23 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_contributor_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='projet_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
            preserve_default=False,
        ),
    ]
