# Generated by Django 5.1.4 on 2024-12-16 14:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_email_user_user_email_unique_constraint"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "Користувач",
                "verbose_name_plural": "Користувачі",
            },
        ),
    ]
