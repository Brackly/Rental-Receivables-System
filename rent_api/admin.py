from django.contrib import admin
from.models import Tenant,House,Landlord,Payments,Month,Year,Invoice

# Register your models here.

admin.site.register(Tenant)
admin.site.register(House)
admin.site.register(Landlord)
admin.site.register(Payments)
admin.site.register(Month)
admin.site.register(Year)
admin.site.register(Invoice)

