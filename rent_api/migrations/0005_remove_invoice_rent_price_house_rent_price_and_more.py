# Generated by Django 4.0.4 on 2022-05-13 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_api', '0004_month_year_rename_apartment_house_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='Rent_price',
        ),
        migrations.AddField(
            model_name='house',
            name='Rent_price',
            field=models.FloatField(default=10500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='deposit',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]