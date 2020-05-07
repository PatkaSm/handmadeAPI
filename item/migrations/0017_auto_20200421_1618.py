# Generated by Django 3.0.5 on 2020-04-21 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0016_auto_20200421_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Brązowy', 'Brązowy'), ('Fioletowy', 'Fioletowy'), ('Niebieski', 'Niebieski'), ('Czerwony', 'Czerwony'), ('Zielony', 'Zielony'), ('Biały', 'Biały'), ('Żółty', 'Żółty'), ('Różowy', ' Różowy'), ('Czarny', 'Czarny')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('do 30 dni', 'do 30 dni'), ('1-3 dni', '1-3 dni'), ('do 7 dni', 'do 7 dni')], max_length=255),
        ),
    ]