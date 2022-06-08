# Generated by Django 3.1.7 on 2021-05-18 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datlien', '0012_auto_20210518_2004'),
        ('user', '0016_remove_delivery_delivery_boy'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAgent',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.delivery')),
                ('delivery_boy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='datlien.deliveryboy')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]