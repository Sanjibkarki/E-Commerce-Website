# Generated by Django 4.2.6 on 2023-12-22 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posti', '0013_ordermodel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='user',
        ),
    ]
