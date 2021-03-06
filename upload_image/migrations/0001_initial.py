# Generated by Django 3.0.5 on 2020-04-17 12:29

from django.db import migrations, models
import django.db.models.deletion
import upload_image.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to=upload_image.models.upload_location)),
                ('offer', models.ForeignKey(blank=None, on_delete=django.db.models.deletion.CASCADE, to='offer.Offer')),
            ],
        ),
    ]
