# Generated by Django 4.2.6 on 2023-10-30 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posti', '0008_alter_ordermodel_pprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
