# Generated by Django 3.0.5 on 2020-04-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
