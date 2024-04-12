# Generated by Django 4.2.6 on 2023-12-21 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_transaction_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['expense_type']},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='expense_type',
            field=models.CharField(choices=[('Credit', 'Credit'), ('Debit', 'Debit')], default='Debit', max_length=10),
        ),
    ]