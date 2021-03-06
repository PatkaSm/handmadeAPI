# Generated by Django 3.0.5 on 2020-04-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_auto_20200421_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Czerwony', 'Czerwony'), ('Brązowy', 'Brązowy'), ('Fioletowy', 'Fioletowy'), ('Różowy', ' Różowy'), ('Zielony', 'Zielony'), ('Niebieski', 'Niebieski'), ('Czarny', 'Czarny'), ('Biały', 'Biały'), ('Żółty', 'Żółty')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('1-3 dni', '1-3 dni'), ('do 30 dni', 'do 30 dni'), ('do 7 dni', 'do 7 dni')], max_length=255),
        ),
    ]
