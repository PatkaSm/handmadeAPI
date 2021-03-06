# Generated by Django 3.0.5 on 2020-04-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_auto_20200421_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Różowy', ' Różowy'), ('Żółty', 'Żółty'), ('Biały', 'Biały'), ('Brązowy', 'Brązowy'), ('Czarny', 'Czarny'), ('Czerwony', 'Czerwony'), ('Fioletowy', 'Fioletowy'), ('Zielony', 'Zielony'), ('Niebieski', 'Niebieski')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('do 7 dni', 'do 7 dni'), ('do 30 dni', 'do 30 dni'), ('1-3 dni', '1-3 dni')], max_length=255),
        ),
    ]
