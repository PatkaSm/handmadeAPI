# Generated by Django 3.0.5 on 2020-06-03 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0030_auto_20200530_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Żółty', 'Żółty'), ('Czarny', 'Czarny'), ('Czerwony', 'Czerwony'), ('Niebieski', 'Niebieski'), ('Zielony', 'Zielony'), ('Brązowy', 'Brązowy'), ('Różowy', 'Różowy'), ('Biały', 'Biały'), ('Fioletowy', 'Fioletowy')], max_length=255),
        ),
    ]