# Generated by Django 3.1.7 on 2021-05-18 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210518_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='d_address',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='d_contact',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='d_person',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='type',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='weight',
        ),
    ]