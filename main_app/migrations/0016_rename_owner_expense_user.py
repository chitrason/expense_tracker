# Generated by Django 3.2.7 on 2021-09-05 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_alter_expense_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='owner',
            new_name='user',
        ),
    ]
