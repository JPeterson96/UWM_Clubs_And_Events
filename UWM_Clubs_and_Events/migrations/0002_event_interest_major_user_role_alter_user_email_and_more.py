# Generated by Django 4.2.5 on 2023-10-05 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("UWM_Clubs_and_Events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, unique=True)),
                ("organization", models.CharField(max_length=30)),
                ("location", models.CharField(max_length=30)),
                ("time", models.DateTimeField()),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Interest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag", models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Major",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                ("department", models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Student"), (1, "Organization")], default=0
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name="UserMajor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "major",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UWM_Clubs_and_Events.major",
                        to_field="name",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UWM_Clubs_and_Events.user",
                        to_field="email",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserInterest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UWM_Clubs_and_Events.interest",
                        to_field="tag",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UWM_Clubs_and_Events.user",
                        to_field="email",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UWM_Clubs_and_Events.event",
                        to_field="name",
                    ),
                ),
                (
                    "interest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UWM_Clubs_and_Events.interest",
                        to_field="tag",
                    ),
                ),
            ],
        ),
    ]