# Generated by Django 4.2.6 on 2023-12-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_income_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='transaction',
            name='balance',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]