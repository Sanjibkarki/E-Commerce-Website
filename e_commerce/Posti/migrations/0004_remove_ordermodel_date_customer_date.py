# Generated by Django 4.2.6 on 2023-10-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posti', '0003_remove_ordermodel_customer_ordermodel_pname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='date',
        ),
        migrations.AddField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
