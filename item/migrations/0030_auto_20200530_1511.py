# Generated by Django 3.0.5 on 2020-05-30 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0029_auto_20200528_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='shipping_abroad',
        ),
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Biały', 'Biały'), ('Niebieski', 'Niebieski'), ('Czarny', 'Czarny'), ('Czerwony', 'Czerwony'), ('Różowy', 'Różowy'), ('Zielony', 'Zielony'), ('Fioletowy', 'Fioletowy'), ('Żółty', 'Żółty'), ('Brązowy', 'Brązowy')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.CharField(choices=[('do 7 dni', 'do 7 dni'), ('1-3 dni', '1-3 dni'), ('do 30 dni', 'do 30 dni')], max_length=255),
        ),
    ]
