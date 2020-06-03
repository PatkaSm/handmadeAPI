# Generated by Django 3.0.5 on 2020-06-03 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0032_auto_20200603_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Biały', 'Biały'), ('Czarny', 'Czarny'), ('Zielony', 'Zielony'), ('Brązowy', 'Brązowy'), ('Fioletowy', 'Fioletowy'), ('Niebieski', 'Niebieski'), ('Żółty', 'Żółty'), ('Czerwony', 'Czerwony'), ('Różowy', 'Różowy')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('do 30 dni', 'do 30 dni'), ('1-3 dni', '1-3 dni'), ('do 7 dni', 'do 7 dni')], max_length=255),
        ),
    ]
