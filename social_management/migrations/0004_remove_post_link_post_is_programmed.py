# Generated by Django 5.1.1 on 2024-10-20 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_management', '0003_post_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='link',
        ),
        migrations.AddField(
            model_name='post',
            name='is_programmed',
            field=models.BooleanField(default=False),
        ),
    ]
