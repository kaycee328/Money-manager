# Generated by Django 4.2.6 on 2023-12-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_alter_profile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='income',
            field=models.FloatField(),
        ),
    ]
