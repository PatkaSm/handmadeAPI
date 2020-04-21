# Generated by Django 3.0.5 on 2020-04-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20200418_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Czerwony', 'Czerwony'), ('Zielony', 'Zielony'), ('Różowy', ' Różowy'), ('Czarny', 'Czarny'), ('Brązowy', 'Brązowy'), ('Żółty', 'Żółty'), ('Fioletowy', 'Fioletowy'), ('Biały', 'Biały'), ('Niebieski', 'Niebieski')], max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='ready_in',
            field=models.IntegerField(choices=[('2', 'do 7 dni'), ('3', 'do 30 dni'), ('1', '1-3 dni')]),
        ),
    ]
