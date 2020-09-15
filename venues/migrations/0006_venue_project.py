# Generated by Django 2.2.10 on 2020-04-08 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
        ("venues", "0005_alter_name_translation"),
    ]

    operations = [
        migrations.AddField(
            model_name="venue",
            name="project",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="venues",
                to="projects.Project",
                verbose_name="project",
            ),
            preserve_default=False,
        ),
    ]