# Generated by Django 2.2.13 on 2020-10-09 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("languages", "0001_initial"),
        ("users", "0006_populate_guardian_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="guardian",
            name="languages_spoken_at_home",
            field=models.ManyToManyField(
                blank=True,
                related_name="guardians",
                to="languages.Language",
                verbose_name="languages spoken at home",
            ),
        ),
    ]
