# Generated by Django 2.2.9 on 2020-01-24 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_event_duration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="duration",
        ),
        migrations.AddField(
            model_name="event",
            name="duration",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="duration", help_text="In minutes"
            ),
        ),
    ]
