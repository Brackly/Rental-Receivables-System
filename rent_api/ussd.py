
from django.http import HttpResponse
from importlib.resources import contents
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
import json


#header('content-type: text/plain')


def explode(text):
    x = text.split("*")
    return x

def count(x):
    level=len(x)
    return level

@csrf_exempt
def ussd(request):
    
    global response
    
    

    session_id = request.POST["sessionId"]
    service_code = request.POST["serviceCode"]
    phone_number = request.POST["phoneNumber"]
    text = request.POST["text"]

    if text == '':
        response  = "CON Select an option to proceed \n"
        response += "1. Tenants \n"
        response += "2. Houses \n"
        response += "3. Payments \n"
        response += "4. My Account"

    elif text == '1':
        response = "CON Select a service to perform \n"
        response += "1. Check a Tenant \n"
        response += "2. Create a Tenant"

    elif text == '2':
        response = "CON Select a service to perform \n"
        response += "1. Check a House \n"
        response += "2. Create a House"

    elif text == '3':
        response = "CON Select a service to perform \n"
        response += "1. Check a Payment \n"
        response += "2. Create a Payment"

    elif text == '4':
        response = "CON Select a service to perform \n"
        response += "1. Check account Balance \n"
        response += "2. Check account status"

    elif text == '1*1':
        response = "CON Enter the Tenant ID "

    elif text == '2*1':
        response = "CON Enter the House ID "

    elif text == '3*1':
        response = "CON Enter the Payment ID " 
     
    elif explode(text)[0]=='1' and explode(text)[1]=='1' and count(explode(text))==3:
        tenant_id = explode(text)[2]
        url='http://127.0.0.1:8000/api/tenants/'+tenant_id
        response=requests.request('GET',url)
        if response.text=="Tenant does not exist":
            response ="END Response: \n"+response.text
        else:
            data=response.json()
            response ="END Tenant Details: \n\n Tenant_name: "+data["Tenant_name"]+"\n Phone number: "+data["Phone_number"]+"\n House number: "+str(data["House_number"])+"\n Start Date: "+str(data["Start_Date"])+"\n Active :"+str(data["Active"])       
        print(response)
    elif explode(text)[0]=='2' and explode(text)[1]=='1' and count(explode(text))==3:
        house_id=explode(text)[2]
        try:
            url='http://127.0.0.1:8000/api/houses/'+house_id
            data=requests.request('GET',url).json()
            response ="END House Details: \n\n House_no: "+data["House_no"]+"\n Description: "+data["Description"]+"\n Occupied: "+str(data["occupied"])+"\n Tenant Id: "+data["Tenant_Id"]+"\n Paid for this Month :"+str(data["Paid_for"])+"\n Cleared :"+str(data["Cleared_payment"])
        except:
            response ="No House with the ID: "+ house_id+" Found"
        print(response)

    elif explode(text)[0]=='3' and explode(text)[1]=='1' and count(explode(text))==3:
        Payment_id = explode(text)[2]
        url='http://127.0.0.1:8000/api/payments/'+Payment_id
        data=requests.request('GET',url).json()
        response="END Payment Details: \n\n Payment ID: "+data["Payment_Id"]+"\n Amount: "+data["Amount"]+"\n Date: "+str(data["Date"])+"\n Mode of Payment: "+data["mode_of_payment"]+"\n Invoiced :"+str(data["Invoiced"])+"\n Paid by :"+data["Tenant_Id"]

    elif text == '4*1':
        response = "CON Choose Month to get Balance " 
        response+="1.This month"
        response+="2.Other month"

    elif text=='4*1*1':
        date=datetime.datetime.now()
        url='http://127.0.0.1:8000/api/dashboard/'+str(date.month)+'/'+str(date.year)
        print(url)
        data=requests.request('GET',url).json()
        response="END Your Account Details: \n Expected Rent: "+str(data["Expected"])+"\n Received Rent : "+str(data["Received"])+"\n Rent Deficit: "+str(data["Deficit"])


    elif text == '4*2':
        status="Active"
        response=status

    elif text == '1*2':
        balance  = "KES 10,000"
        response = "END Your balance is " + balance
    elif text == '2':
        response = "END This is your phone number " + phone_number
    #print(response)

    return HttpResponse(response)