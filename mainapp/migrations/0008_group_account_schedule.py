# Generated by Django 2.2.3 on 2019-08-02 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20190730_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('Group_money', models.IntegerField()),
                ('user', models.ManyToManyField(to='mainapp.User_account')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('penalty', models.IntegerField()),
                ('location', models.CharField(max_length=100, null=True)),
                ('group_ac', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Group_account')),
            ],
        ),
    ]