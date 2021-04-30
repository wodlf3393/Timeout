# Generated by Django 2.2.3 on 2019-07-30 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20190730_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_account',
            name='history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.User_history'),
        ),
        migrations.AlterField(
            model_name='user_account',
            name='user_money',
            field=models.IntegerField(),
        ),
    ]