# Generated by Django 3.0.5 on 2020-04-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0021_auto_20200421_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Różowy', ' Różowy'), ('Czerwony', 'Czerwony'), ('Czarny', 'Czarny'), ('Niebieski', 'Niebieski'), ('Biały', 'Biały'), ('Brązowy', 'Brązowy'), ('Zielony', 'Zielony'), ('Żółty', 'Żółty'), ('Fioletowy', 'Fioletowy')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('1-3 dni', '1-3 dni'), ('do 30 dni', 'do 30 dni'), ('do 7 dni', 'do 7 dni')], max_length=255),
        ),
    ]