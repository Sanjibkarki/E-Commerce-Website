# Generated by Django 4.2.6 on 2023-12-27 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_remove_footwear_size_remove_lowerwear_size_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_mark_returned', 'Set book as returned'),),
            },
        ),
    ]
