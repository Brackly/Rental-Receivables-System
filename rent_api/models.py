from tkinter import CASCADE
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Tenant(models.Model):
    Tenant_Id=models.CharField(max_length=8,primary_key=True)
    Tenant_name=models.CharField(max_length=100)
    Phone_number=models.CharField(max_length=13)
    Email=models.CharField(max_length=30)
    Next_of_kin=models.CharField(max_length=100)
    Nok_phone_number=models.CharField(max_length=13)
    House_number=models.ForeignKey('House',on_delete=models.CASCADE,null=True)
    Start_Date=models.DateField(auto_now_add=True)
    End_Date=models.DateField(auto_now_add=True)
    Active=models.BooleanField(default=False)
    def __str__(self):
        return (self.Tenant_name)

class Landlord(models.Model):
    Landlord_Id=models.CharField(max_length=8,primary_key=True)
    Landlord_name=models.CharField(max_length=100)
    Phone_number=models.CharField(max_length=13)
    Landlord_code=models.CharField(max_length=20)
    Apartment=models.CharField(max_length=20)
    def __str__(self):
        return (self.Landlord_name)


class Payments(models.Model):
    Payment_Id=models.CharField(max_length=20,primary_key=True)
    Amount=models.CharField(max_length=20)
    Date=models.DateField(auto_now_add=True)
    mode_of_payment = models.CharField(max_length=20)
    Invoiced=models.BooleanField(default=False)
    House_no=models.ForeignKey('House',on_delete=models.CASCADE,null=True)
    Tenant_Id=models.ForeignKey('Tenant',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return (self.Payment_Id)

class House(models.Model):
    House_no=models.CharField(max_length=20,primary_key=True)
    Description=models.CharField(max_length=20)
    Rent_price=models.FloatField()
    deposit=models.IntegerField()
    occupied=models.BooleanField(default=False)
    Tenant_Id=models.CharField(max_length=20,null=True)
    Paid_for=models.BooleanField(default=False,null=True)
    Cleared_payment=models.BooleanField(default=False,null=True)
    def __str__(self):
        return (self.House_no)

class Month(models.Model):
    Month_ID=models.CharField(max_length=2,primary_key=True)
    Month_name=models.CharField(max_length=20)
    def __str__(self):
        return (self.Month_name)

class Year(models.Model):
    Year_name=models.CharField(max_length=20,primary_key=True)
    def __str__(self):
        return (self.Year_name)

class Invoice(models.Model):
    Invoice_ID=models.CharField(max_length=20,primary_key=True)
    Month_ID=models.ForeignKey('Month',on_delete=models.CASCADE)
    Year_name=models.ForeignKey('Year',on_delete=models.CASCADE)
    House_no=models.ForeignKey('House',on_delete=models.CASCADE)
    Active=models.BooleanField(default=True)
    Opening_balance=models.FloatField()
    Closing_balance=models.FloatField()
    Total_Payments=models.FloatField()
    def __str__(self):
        return (self.House_no)




    
