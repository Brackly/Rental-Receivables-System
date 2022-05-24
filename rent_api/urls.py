from django.urls import path,include
from .import views
from .import ussd

urlpatterns=[
    path('payments/',views.paymentList, name="payments"),
    path('payments/<str:pk>/',views.paymentDetail, name="payment_detail"),
    path('create-payment/',views.createPayment, name="create_payments"),
    path('tenants/',views.tenantList, name="tenants"),
    path('tenants/<str:pk>/',views.tenantDetail, name="tenants_detail"),
    path('create-tenant/',views.createTenant, name="create_payments"),
    path('houses/',views.houseList, name="houses"),
    path('houses/<str:pk>/',views.houseDetail, name="houses_detail"),
    path('create-house/',views.createHouse, name="create_payments"),
    path('invoice/<str:house_no>/<str:month>/<str:year>/',views.houseInvoice,name="invoice"),
    #path('tenants/deactivate/<str:tenant_id>/',views.tenantDeactivate,name="deactivate_tenant")
    path('getbalance/<str:house_no>/<str:month>/<str:year>/',views.getUnitBalance, name="getBalance"),
    path('dashboard/<str:month>/<str:year>/',views.DashBalance, name="dashBalance"),
    path('newmonth/<str:month>/<str:year>/',views.newMonth, name="newMonth"),
    path('ussd/',ussd.ussd,name="ussd")
]