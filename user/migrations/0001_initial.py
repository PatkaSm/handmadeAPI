# Generated by Django 3.0.5 on 2021-01-27 18:50

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('nickname', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, default='default.png', upload_to=user.models.upload_location)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
