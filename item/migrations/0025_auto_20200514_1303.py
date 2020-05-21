# Generated by Django 3.0.5 on 2020-05-14 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0024_auto_20200514_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Żółty', 'Żółty'), ('Biały', 'Biały'), ('Czerwony', 'Czerwony'), ('Czarny', 'Czarny'), ('Zielony', 'Zielony'), ('Niebieski', 'Niebieski'), ('Fioletowy', 'Fioletowy'), ('Różowy', ' Różowy'), ('Brązowy', 'Brązowy')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('do 7 dni', 'do 7 dni'), ('1-3 dni', '1-3 dni'), ('do 30 dni', 'do 30 dni')], max_length=255),
        ),
    ]