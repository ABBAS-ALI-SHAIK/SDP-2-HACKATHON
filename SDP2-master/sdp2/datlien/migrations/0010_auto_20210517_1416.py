# Generated by Django 3.1.7 on 2021-05-17 08:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datlien', '0009_auto_20210517_1356'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Account',
        ),
    ]