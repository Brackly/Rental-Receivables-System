# Generated by Django 4.0.4 on 2022-05-14 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rent_api', '0007_alter_payments_house_no_alter_payments_tenant_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payments',
            old_name='Complete',
            new_name='Invoiced',
        ),
    ]
