# Generated by Django 3.0.7 on 2020-06-29 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="password",
            field=models.BooleanField(default=False),
        ),
    ]
