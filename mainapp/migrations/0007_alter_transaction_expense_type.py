# Generated by Django 4.2.6 on 2023-12-21 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_profile_rename_category_transaction_expense_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='expense_type',
            field=models.BooleanField(choices=[('Positive', 'Positive'), ('Negative', 'Negative')], default=False),
        ),
    ]
