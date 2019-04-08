# Generated by Django 2.1.7 on 2019-04-08 20:06

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0002_auto_20190328_0459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='second_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                   max_length=150, unique=True,
                                   validators=[django.contrib.auth.validators.UnicodeUsernameValidator()]),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(related_name='users', to='authentication.Role'),
        ),
    ]