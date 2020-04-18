# Generated by Django 3.0.5 on 2020-04-18 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('Różowy', ' Różowy'), ('Brązowy', 'Brązowy'), ('Czerwony', 'Czerwony'), ('Czarny', 'Czarny'), ('Niebieski', 'Niebieski'), ('Fioletowy', 'Fioletowy'), ('Biały', 'Biały'), ('Żółty', 'Żółty'), ('Zielony', 'Zielony')], default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='ready_in',
            field=models.IntegerField(choices=[(1, 'do 7 dni'), (1, '1-3 dni')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='shipping_abroad',
            field=models.BooleanField(default=False),
        ),
    ]