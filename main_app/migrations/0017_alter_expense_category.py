# Generated by Django 3.2.7 on 2021-09-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_rename_owner_expense_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(max_length=250),
        ),
    ]
