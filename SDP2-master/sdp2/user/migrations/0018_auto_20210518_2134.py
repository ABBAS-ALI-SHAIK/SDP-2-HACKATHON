# Generated by Django 3.1.7 on 2021-05-18 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_deliveryagent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryagent',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.delivery', verbose_name='Package Id'),
        ),
    ]
