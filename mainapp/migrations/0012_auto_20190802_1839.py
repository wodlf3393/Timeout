# Generated by Django 2.2.3 on 2019-08-02 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20190802_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group_account',
            old_name='use',
            new_name='members',
        ),
        migrations.RenameField(
            model_name='user_account',
            old_name='user',
            new_name='name',
        ),
    ]
