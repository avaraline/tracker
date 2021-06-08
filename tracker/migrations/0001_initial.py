# Generated by Django 3.0.2 on 2020-01-23 23:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
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
                ("address", models.GenericIPAddressField()),
                ("port", models.IntegerField()),
                ("first_seen", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_seen", models.DateTimeField(default=django.utils.timezone.now)),
                ("players", models.TextField(blank=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "unique_together": {("address", "port")},
            },
        ),
    ]
