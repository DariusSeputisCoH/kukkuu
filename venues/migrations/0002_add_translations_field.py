# Generated by Django 2.2.8 on 2020-01-16 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venues", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="venue",
            name="description",
        ),
        migrations.RemoveField(
            model_name="venue",
            name="name",
        ),
        migrations.CreateModel(
            name="VenueTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "master",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="venues.Venue",
                    ),
                ),
            ],
            options={
                "verbose_name": "venue Translation",
                "db_table": "venues_venue_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
        ),
    ]
