# Generated by Django 4.2.6 on 2023-12-21 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0005_alter_transaction_options_transaction_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.FloatField()),
                ('balance', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='category',
            new_name='expense_type',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.DeleteModel(
            name='Income',
        ),
    ]