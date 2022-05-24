from dataclasses import fields
from rest_framework import serializers
from .models import Tenant,Payments,House,Month,Year,Invoice

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tenant
        fields='__all__'  
class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model=House
        fields='__all__'
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields='__all__'
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invoice
        fields='__all__'

