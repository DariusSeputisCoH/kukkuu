# Generated by Django 2.2.8 on 2020-01-13 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Venue",
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
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated_at"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("seat_count", models.PositiveIntegerField(verbose_name="seat count")),
            ],
            options={
                "verbose_name": "venue",
                "verbose_name_plural": "venues",
            },
        ),
    ]
