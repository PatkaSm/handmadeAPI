# Generated by Django 3.0.5 on 2020-04-21 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_auto_20200421_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Biały', 'Biały'), ('Czerwony', 'Czerwony'), ('Żółty', 'Żółty'), ('Niebieski', 'Niebieski'), ('Brązowy', 'Brązowy'), ('Fioletowy', 'Fioletowy'), ('Zielony', 'Zielony'), ('Czarny', 'Czarny'), ('Różowy', ' Różowy')], max_length=255),
        ),
    ]
