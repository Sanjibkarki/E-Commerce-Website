# Generated by Django 4.2.6 on 2023-10-23 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posti', '0005_alter_customer_date_alter_ordermodel_pprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(auto_created=True, verbose_name='date-published'),
        ),
    ]