# Generated by Django 2.2.3 on 2019-07-30 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20190730_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_account',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]