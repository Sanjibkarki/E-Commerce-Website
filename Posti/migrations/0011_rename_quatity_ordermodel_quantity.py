# Generated by Django 4.2.6 on 2023-10-31 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posti', '0010_ordermodel_quatity_ordermodel_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermodel',
            old_name='Quatity',
            new_name='Quantity',
        ),
    ]
