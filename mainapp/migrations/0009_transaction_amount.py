# Generated by Django 4.2.6 on 2023-12-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_alter_transaction_expense_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]