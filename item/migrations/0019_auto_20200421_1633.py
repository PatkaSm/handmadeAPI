# Generated by Django 3.0.5 on 2020-04-21 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0018_auto_20200421_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Brązowy', 'Brązowy'), ('Biały', 'Biały'), ('Niebieski', 'Niebieski'), ('Czerwony', 'Czerwony'), ('Żółty', 'Żółty'), ('Czarny', 'Czarny'), ('Różowy', ' Różowy'), ('Fioletowy', 'Fioletowy'), ('Zielony', 'Zielony')], max_length=255),
        ),
    ]