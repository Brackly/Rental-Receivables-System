# Generated by Django 4.0.4 on 2022-04-24 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('House_no', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Apartment', models.CharField(max_length=20)),
                ('occupied', models.BooleanField(default=False)),
                ('Tenant_Id', models.CharField(max_length=20, null=True)),
                ('Paid_for', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('Landlord_Id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('Landlord_name', models.CharField(max_length=100)),
                ('Phone_number', models.CharField(max_length=13)),
                ('Landlord_code', models.CharField(max_length=20)),
                ('Apartment', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('Tenant_Id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('Tenant_name', models.CharField(max_length=100)),
                ('Phone_number', models.CharField(max_length=13)),
                ('Next_of_kin', models.CharField(max_length=100)),
                ('Nok_phone_number', models.CharField(max_length=13)),
                ('Landlord_code', models.CharField(max_length=20)),
                ('House_number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_api.house')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('Payment_Id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Amount', models.CharField(max_length=20)),
                ('Date', models.DateField(auto_now_add=True)),
                ('mode_of_payment', models.CharField(choices=[('MPESA', 'MPESA'), ('BANK', 'BANK')], max_length=20)),
                ('Month', models.CharField(max_length=20)),
                ('House_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_api.house')),
                ('Tenant_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_api.tenant')),
            ],
        ),
    ]
