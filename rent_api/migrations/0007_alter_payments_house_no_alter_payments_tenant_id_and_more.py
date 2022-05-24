# Generated by Django 4.0.4 on 2022-05-14 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rent_api', '0006_invoice_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='House_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_api.house'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='Tenant_Id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_api.tenant'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='House_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_api.house'),
        ),
    ]