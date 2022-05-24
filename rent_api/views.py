from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rent_api.models import Payments,Tenant,Landlord,House,Invoice,Month,Year
from .serializers import TenantSerializer,PaymentsSerializer,HouseSerializer,InvoiceSerializer
import datetime
from .ussd import ussd
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def getPreviousDetails(month,year):
    if month==1:
        month=12
        year=year-1
    else:
        month=int(month)-1
        year=year
    previousDetails={"month":month,"year":year}
    return previousDetails

    

def updateInvoice(amount,house_no,month,year):
    invoice=Invoice.objects.get(House_no=house_no,Month_ID=month,Year_name=year)
    if invoice.Active==True:
        invoice.Total_Payments+=int(amount)
        invoice.save()
        invoice.Closing_balance=invoice.Opening_balance-invoice.Total_Payments
        invoice.save()
        setStatus(house_no,month,year)

def checkHouseAvailability(house_no):
    house_exists=House.objects.filter(House_no=house_no).exists()
    print(house_exists)
    if house_exists==True:
        house=House.objects.get(House_no=house_no)
        if house.occupied==False:
            return True
        elif house.occupied==True:
            err="This House is already House Occupied"
            return (err)
    elif house_exists!=True:
        err="This house Does Not Exist!! "
        return (err)

def unoccupyHouse(initial):
    old_house=House.objects.get(House_no=initial)
    old_house.occupied=False
    old_house.Tenant_Id=None
    old_house.Paid_for=None
    old_house.Cleared_payment=None

    old_house.save()


def changeHouses(house_no,initial,tenant_id):
    old_house=House.objects.get(House_no=initial)
    new_house=House.objects.get(House_no=house_no)

    new_house.occupied=True
    new_house.Tenant_Id=tenant_id
    new_house.Paid_for=old_house.Paid_for
    new_house.Cleared_payment=old_house.Cleared_payment

    new_house.save()

    unoccupyHouse(initial)
    initializeHouseInvoice(house_no,tenant_id)
    deactivateInvoice(initial)

def deactivateInvoice(initial):
    invoice=Invoice.objects.get(House_no=initial)
    if invoice.Active==True:
        invoice.Active=False
        invoice.save()
   
def initializeTenantHouse(tenant_id,house_no):
    #print(tenant_id)
    date=getDate()
    initializeHouseInvoice(house_no,tenant_id)
    new_occupied_house=House.objects.get(House_no=house_no)
    new_occupied_house.occupied=True
    new_occupied_house.Tenant_Id=tenant_id
    new_occupied_house.Paid_for=checkHousePaidFor(house_no,date.month,date.year)
    new_occupied_house.Cleared_payment=checkHouseClearedFor(house_no,date.month,date.year)

    new_occupied_house.save()

def checkHousePaidFor(house_no,month,year):
    invoice=Invoice.objects.get(House_no=house_no,Month_ID=month,Year_name=year)
    if invoice.Active==True:
        if invoice.Total_Payments>0:
            return True
            print("True")
        else:
            return False
            print("False")

def checkHouseClearedFor(house_no,month,year):
    invoice=Invoice.objects.get(House_no=house_no,Month_ID=month,Year_name=year)
    if invoice.Active==True:
        if invoice.Closing_balance>0:
            return False
        else:
            return True

def getDate():
    date=datetime.datetime.now()
    return date

def newInvoice(tenant_id,house_no,amount,month,year):
    invoice=Invoice(
        Invoice_ID=str(tenant_id)+str(year)+str(month),
        Month_ID=Month.objects.get(Month_ID=month),
        Year_name=Year.objects.get(Year_name=year),
        House_no=House.objects.get(House_no=house_no),
        Opening_balance=amount,
        Total_Payments=0,
        Closing_balance=amount
        )
    invoice.save()

def initializeRent(month,year):
    previousDetails=getPreviousDetails(month,year)
    invoices=Invoice.objects.filter(Month_ID=previousDetails["month"],Year_name=previousDetails["year"])
    for invoice in invoices:
        if invoice.Active==True:
            tenant=Tenant.objects.get(House_number=invoice.House_no)
            house=House.objects.get(House_no=invoice.House_no)
            arrears=invoice.Closing_balance
            amount=house.Rent_price+arrears
            newInvoice(tenant.Tenant_Id,invoice.House_no,amount,month,year)

    

def initializeHouseInvoice(house_no,tenant_id):
    date=datetime.datetime.now()
    month=date.month
    year=date.year
    new_house=House.objects.get(House_no=house_no)
    amount=new_house.Rent_price+(new_house.Rent_price*new_house.deposit)
    newInvoice(tenant_id,house_no,amount,month,year)
    
def collectPayments(url):
    incoming_payments=[]
    incoming_payments=url
    for incoming_payment in incoming_payments:
        payment=Payments(

        )

def setStatus(house_no,month,year):
    house=House.objects.get(House_no=house_no)
    paid=checkHousePaidFor(house.House_no,month,year)
    cleared=checkHouseClearedFor(house.House_no,month,year)
    if paid==True:
        if cleared==True:
            house.Paid_for=True
            house.Cleared_payment=True
            house.save()  
        elif cleared==False:
            house.Paid_for=True
            house.Cleared_payment=False
            house.save() 
    else:
        house.Paid_for=False
        house.Cleared_payment=False
        house.save()

def TotalBalances(month,year):
    invoices=Invoice.objects.filter(Month_ID=month,Year_name=year)
    Expected=0
    Received=0
    Deficit=0
    for invoice in invoices:
        if invoice.Active==True:
            Expected+=invoice.Opening_balance
            Received+=invoice.Total_Payments
            Deficit+=invoice.Closing_balance
    data={"Expected":Expected,"Received":Received,"Deficit":Deficit}
    return data

    


def UnitBalance(house_no,month,year):
    invoice=Invoice.objects.get(House_no=house_no,Month_ID=month,Year_name=year)
    if invoice.Active==True:
        payments=invoice.Total_Payments
        arrears=invoice.Closing_balance
        unit_data={"Total Payments":payments,"Arrears":arrears}
        return unit_data


    
    
    #total for one house
    


#<------------------------------------------------------------------------------------------------------------>

@api_view(['GET'])
def paymentList(request):
    payments=Payments.objects.all()
    serializer=PaymentsSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def DashBalance(request,month,year):
    total=TotalBalances(month,year)
    return Response(total)

@api_view(['POST'])
def createPayment(request):
    serializer=PaymentsSerializer(data=request.data)

    amount=request.data["Amount"]
    house_no=request.data["House_no"]

    if serializer.is_valid():
        date=getDate()
        updateInvoice(amount,house_no,date.month,date.year)
        request.data["Invoiced"]=True
        serializer.save()
    return Response(serializer.data)
  

@api_view(['GET','DELETE','PUT'])
def paymentDetail(request,pk):
    payment=Payments.objects.get(Payment_Id=pk)
    

    if request.method=='DELETE':
        amount=0-int(payment.Amount)
        house_no=payment.House_no
        invoiced=payment.Invoiced

        date=getDate()
        updateInvoice(amount,house_no,date.month,date.year)
        payment.delete()
        return Response("ITEM DELETED")

    elif request.method=='GET':
        serializer=PaymentsSerializer(payment, many=False)

    elif request.method=='PUT':
        serializer=PaymentsSerializer(instance=payment,data=request.data)
        amount=int(request.data["Amount"])-int(payment.Amount)
        house_no=request.data["House_no"]
        invoiced=request.data["Invoiced"] 

        if serializer.is_valid():
            serializer.save()
            date=getDate()
            updateInvoice(amount,house_no,date.month,date.year)
            return Response("ITEM UPDATED")

    return Response(serializer.data)

@api_view(['GET'])
def tenantList(request):
    tenants=Tenant.objects.all()
    serializer=TenantSerializer(tenants, many=True)
    return Response(serializer.data)

@api_view(['GET','DELETE','PUT'])
def tenantDetail(request,pk):
    pk_exists=House.objects.filter(Tenant_Id=pk).exists()
    if pk_exists==True:
        tenant=Tenant.objects.get(Tenant_Id=pk)
        if request.method=='GET':
            serializer=TenantSerializer(tenant, many=False)
            return Response(serializer.data)

        elif request.method=='PUT':
            serializer=TenantSerializer(instance=tenant,data=request.data)
            house_no=request.data["House_number"]
            print(house_no)
            if serializer.is_valid():
                initial=tenant.House_number
                print(initial)
                if house_no==str(initial):
                    print('Hooray')
                    serializer.save()
                    return Response("Tenant Details Updated")
                elif house_no!=str(initial):
                    house=checkHouseAvailability(house_no)
                    print(house)
                    if house==True:
                        changeHouses(house_no,initial,tenant.Tenant_Id)
                        serializer.save()
                        return Response("Tenant saved")
                    else:
                        err=house
                        return Response(err)
            return Response("This house Does not Exist!!")   
    else:
        return Response("Tenant does not exist")    

@api_view(['POST'])
def createTenant(request):
    serializer=TenantSerializer(data=request.data)
    house_no=request.data["House_number"]
    tenant_id=request.data["Tenant_Id"]

    if serializer.is_valid():
        house=checkHouseAvailability(house_no)
        print(house)
        if house==True:
            initializeTenantHouse(tenant_id,house_no)
            serializer.save()
            tenant=Tenant.objects.get(Tenant_Id=tenant_id)
            tenant.Active=True
            tenant.save()
            print(tenant.Active)
            return Response("Tenant saved")
        else:
            err=house
            print('error:'+err)
            return Response(err)
    return Response("Error occured")
  

@api_view(['GET'])
def houseList(request):
    houses=House.objects.all()
    serializer=HouseSerializer(houses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUnitBalance(request,house_no,month,year):
    unit_data=UnitBalance(house_no,month,year)
    return Response(unit_data)

@api_view(['GET','DELETE','PUT'])
def houseDetail(request,pk):
    house=House.objects.get(House_no=pk)
    if request.method=='GET':
        serializer=HouseSerializer(house, many=False)
        return Response(serializer.data)
    elif request.method=='DELETE':
        if house.occupied==True:
            return Response("Cannot Delete this house because it is occupied!!")
        elif house.occupied==False:
          house.delete()  

@api_view(['POST'])
def createHouse(request):
    serializer=HouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
  

@api_view(['GET'])
def houseInvoice(request,house_no,month,year):
    invoice=Invoice.objects.filter(House_no=house_no, Year_name=year ,Month_ID=month)
    serializer=InvoiceSerializer(invoice, many=True)
    return Response(serializer.data)


def tenantDeactivate(request,tenant_id):
    
    tenant=Tenant.objects.get(Tenant_Id=tenant_id)
    if tenant.Active==False:
        return redirect('tenants')
    else:
        house=House.objects.filter(Tenant_Id=tenant_id).exists()
        
        house=House.objects.get(Tenant_Id=tenant_id)
        #delink from house occupied
        initial=house.House_no
        unoccupyHouse(initial)

        #Deactivate invoice status
        deactivateInvoice(initial)

        #deactivate tenant status
        tenant.House_number=None
        tenant.End_Date=getDate()
        tenant.Active=False
    tenant.save()

    return redirect('tenants')

@api_view(['GET'])
def newMonth(request,month,year):
    initializeRent(month,year)
    return Response("Success")







