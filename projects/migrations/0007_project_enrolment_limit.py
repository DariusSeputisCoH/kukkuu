# Generated by Django 3.2.8 on 2022-02-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_add_manage_event_groups_perm"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="enrolment_limit",
            field=models.PositiveSmallIntegerField(
                default=2,
                help_text="How many times a single user can participate events per year. Changing this will not affect any existing enrolments.",
                verbose_name="enrolment limit",
            ),
        ),
    ]