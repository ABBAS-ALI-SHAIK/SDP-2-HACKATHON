# Generated by Django 3.1.7 on 2021-05-17 07:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210513_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='date',
        ),
        migrations.AddField(
            model_name='delivery',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]