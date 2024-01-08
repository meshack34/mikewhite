import json
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework import status
import urllib.parse
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from .mpesa.utils import encrypt_security_credential, mpesa_access_token, format_phone_number, api_base_url, mpesa_config, mpesa_response
import csv
from .models import Dialer
# Create your views here.
empty = 'END Parameters required,MSISN,SESSION_ID,USERDATA'
response = 'End User Input required'
text = ''
cl = MpesaClient()
stk_push_callback_url = 'https://www.kopaloanswin.xyz/'
b2c_callback_url = 'https://darajambili.herokuapp.com/b2c/result'
phone_number = ''



@csrf_exempt
@api_view(['GET', 'POST'])
def cbc(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("phoneNumber")
        INPUT = request.POST.get("text")
        print(INPUT)
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
    
            # print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
                response ="CON Welcome To  FARMMTEC Society\n1. English\n2. Kiswahili" # note the NEW LINE \n

                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33

            elif len(inputArray)==1:
                # Register option
                # Input validation and business logic can go here
                response ="CON Please  Enter Your Full Name"

           # elif (lastInput.isalpha()):
           #     response = "CON Please Enter Your Phone Number "
            elif len(inputArray)==2:
                response = "CON Enter Your Id Number"
             # response = f"CON Please Confirm That this are Your  Details\nname:{name}\nphoneNumber:{phone}\nIdno:{id} \n1.Confirm\n2.Cancel"
            elif len(inputArray)==3:
                response = "CON Dear customer You have been registered to Farmetec Society \n1.Proceed \n2.Done"
            elif len(inputArray)==4:
                response = "CON Check Membership Status \n1. Activate Membership \2.Renew Membership"

            elif len(inputArray)==5:
                response = "End Your Request Has been Received And you will receive Further InformationnFrom Us"
                #stk_push_success(request)
            # elif (len(inputArray)==7 and lastInput == "1"):
            #      response = response = "END You Have Subscribe to 10 Mbs for Sh.1000 for 30days\n"
            # elif lastInput == "2" and len(inputArray) == 2:
            #      # Support contact request
            #      response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
        else:
            response = "END Check your input Details."
            stk_push_success(request)

        return HttpResponse(response,content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})


inputArray = []
@csrf_exempt
@api_view(['GET', 'POST'])
def bund(request):
    if request.method == 'POST':
        global INPUT
        global lastInput
        global MSISDN
        global inputArray

        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("msisdn")
        INPUT = request.POST.get("input")
        print(INPUT)
        print(MSISDN)

        if INPUT is not None:
            inputArray.append(INPUT)
            lastInput = inputArray[-1]  # Get the last element of inputArray

            print(MSISDN)
            print(lastInput)

            if lastInput == '34':
                response = "CON Welcome to instafel checker\n1. English\n2. Kiswahili"
            elif len(inputArray)==2:
                response = f"CON Check {inputArray} Credit Score\n1. Credit Score\n2. Crb Check"
            elif len(inputArray) == 3:
                response =  "CON Please Enter Your Full Name"
            elif len(inputArray) == 4:
                response =  "CON Please Enter Your Email"
            elif len(inputArray) == 5:
                response =  "END Please Proceed To pay And your score will be emailed to you."
            elif lastInput ==3:
                response =  "END Contact our support on the following numbers 2547xxxxxxx, 25402xxx"
            else:
                response =  "END You seem to have input wrong credentials. Please try again."

        return HttpResponse(response)

    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})




inputArray = []
@csrf_exempt
@api_view(['GET', 'POST'])
def Airtime_bund(request):
    if request.method == 'POST':
        global INPUT
        global lastInput
        global MSISDN
        global inputArray

        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("msisdn")
        INPUT = request.POST.get("input")
        print(INPUT)
        print(MSISDN)

        if INPUT is not None:
            inputArray.append(INPUT)
            lastInput = inputArray[-1]  # Get the last element of inputArray

            print(MSISDN)
            print(lastInput)

            if lastInput == '34':
                response = "CON WELCOME TO Smarks Airtime And Bundles Resellers\n1. Buy Airtime\n2. Buy Bundle\n"
            elif len(inputArray)==2:
                response = "please enter your option\n1. Daily\n2. weekly\n3.monthly"
            elif len(inputArray) == 3:
                response =  "please enter your option\n1. Daily\n2. weekly\n3.monthly"
            elif len(inputArray) == 4:
                response =  "CON Please Enter Your Phone Number: "
            
            elif len(inputArray) ==5:
                response =  "Enter amount : "
            elif len(inputArray) ==6:
                response = f"You have successfully bought {lastInput} of bundles/airtime"
            else:
                response =  "END You seem to have input wrong credentials. Please try again."

        return HttpResponse(response)

    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})


@csrf_exempt
@api_view(['GET', 'POST'])
def score(request):
    if request.method == 'GET':
        global INPUT 
        global MSISDN
        SESSIONID = request.GET.get("session_id")
        USSDCODE = request.GET.get("service_code")
        MSISDN = request.GET.get("MSISDN")
        INPUT = request.GET.get("text")
        inputArray = INPUT.split("*") # the last value after * is what the user entered last
        lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this>
        # this is the entry point
        print(MSISDN)
        print(len(inputArray))
        print(lastInput)
        if Dialer.objects.filter(phone_number=MSISDN).exists():
           pass
        else:
            # There is no entry with the same phone number, create a new Dialer instance and save it
            dialer = Dialer(phone_number=MSISDN)
            dialer.save()  
            # this is the entry point
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1]
            if (lastInput == ""):
                response = f"CON WELCOME TO HOMIKA PESA \n1. Apply Loan\n2. Buy Airtime\n3.Invite Friend\n4.My Account "
            # elif len(inputArray)==1:
            #     response = "CON Please Enter Your FullName "
                #response = f"CON Please confirm that this is your phone number {MSISDN}\n 5.Proceed "

            elif len(inputArray)==1:
                response = "CON Please Enter Your ID Number"
            elif len(inputArray)==2:
                response = "CON Select Loan Type \n1.30 Days loan\n2.90 Days Loan"
            elif len(inputArray)==3:
                response = "CON Your Loan Limit is 55000\n Enter Amount"

            elif len(inputArray)==4:
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
                stk_push_success(request)
                # response = "CON View loan options\n 9. Short-term loan: 5% interest, due in 30 days\n 10. Medium-term loan: 10% interest, due in 90 days\n"
                #print(inputArray[1])
            # elif (lastInput=='9' or lastInput=='10'):
            #     response = "CON Enter loan amount between 1000-15000\n"
            # elif lastInput.isdigit() and 1000 <= int(lastInput) <= 15000:
            #     response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
            #     stk_push_success(request)
            # elif lastInput == "3" and len(inputArray) == 2:
            #     response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx.",
            #     stk_push_success(request)
            else:
                response = "END This option has not been implemented yet. Please try again later."
                stk_push_success(request)
            return HttpResponse(response,content_type='text/plain')
        else:
            return HttpResponse({"error": "Invalid request method. Please use POST."})



@csrf_exempt
def download_csv(request):
    dialers = Dialer.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dialers.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Phone Number',])

    for dialer in dialers:
        writer.writerow([ dialer.phone_number,])

    return response



def dialer_list(request):
    dialers = Dialer.objects.all()
    context = {'dialers': dialers}
    return render(request, 'django_daraja/dialer_list.html', context)

@csrf_exempt
def register_urls(request):
    mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')
    if mpesa_environment == 'sandbox':
        business_short_code = mpesa_config('MPESA_EXPRESS_SHORTCODE')
    else:
        business_short_code = mpesa_config('MPESA_SHORTCODE')
        print(mpesa_access_token)
    #access_token = MpesaAccessToken.validated_mpesa_access_token
    
    r = cl.access_token()
    print(r)
    print(business_short_code)
    l=mpesa_access_token()
    print(l)
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    # headers = {"Authorization": "Bearer %s" % mpesa_access_token}
    headers = {
    'Authorization': 'Bearer ' + l,
    'Content-type': 'application/json'
}
    options = {"ShortCode": business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "http://139.144.227.80/c2b/",
               "ValidationURL": "http://139.144.227.80/validation/"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)



random_number = random.randint(90, 99)
def oauth_success(request):
    r = cl.access_token()
    return JsonResponse(r, safe=False)
        
def stk_push_success(request):
    global MSISDN
    # print(MSISDN)
    random_number = random.randint(90, 99)
    print(random_number)
    phone_number = '0724324545'
    amount = 5
    account_reference = 'SMART LOANS'
    transaction_desc = 'STK Push Description'
    callback_url = stk_push_callback_url
    r = cl.stk_push(phone_number, amount, account_reference,
                    transaction_desc, callback_url)
    return JsonResponse(r.response_description, safe=False)


import json

@csrf_exempt
@api_view(['GET', 'POST'])
def survey(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        request_data = json.loads(request.body)
        SESSIONID = request_data.get("session_id")
        USSDCODE = request_data.get("service_code")
        MSISDN = request_data.get("MSISDN")
        INPUT = request_data.get("ussd_string")
        print(INPUT)
   
        print(MSISDN)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]
        
            print(MSISDN)
            print(len(inputArray))
            
            if (lastInput == ''):
                response = "CON Welcome To Credit Checker\n1. Check Score\n2. Crb Status"
                          
            elif (lastInput=='1' or lastInput=='2'):
                response = "CON Please Enter Your ID Number "
            elif (len(inputArray)==3):
                response = "CON Please Enter Your Full Name"
                # stk_push_success(request)
            elif (len(inputArray)==4):
                response = "CON Please Enter Your Email"
     
            elif len(inputArray)==5:
                response = "END Please Proceed To pay And your scrore will be emailed to you."
                # stk_push_success(request)
            elif lastInput == "3" and len(inputArray) == 2:
                response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
                # stk_push_success(request)
            else:
                response = "END You seem to have input wrong credentials. Please try again."
        else:
            response = "Invalid input received."
        
        return HttpResponse(response)
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})


@csrf_exempt
@api_view(['GET', 'POST'])
def scoe(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("msisdn")
        INPUT = request.POST.get("message")
        print(INPUT)
        if Dialer.objects.filter(phone_number=MSISDN).exists():
            # There is already an entry with the same phone number, do something else
            pass
        else:
            # There is no entry with the same phone number, create a new Dialer instance and save it
            dialer = Dialer(phone_number=MSISDN)
            dialer.save()
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. >
        # this is the entry point
    
            # print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
                response ="CON Welcome To  PROFITKA VENTURES\n1. Get a 7 day loan\n2. Get a 30 days loan" # note the NEW LINE \n

                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33>

            elif ((lastInput == "1" and len(inputArray)==1)or(lastInput == "2" and len(inputArray)==1)):
                # Register option
                # Input validation and business logic can go here
                response ="CON Please  Enter Your FirstName"

           # elif (lastInput.isalpha()):
           #     response = "CON Please Enter Your Phone Number "
            elif lastInput.isalpha():
           #     response = "CON Enter Your Id Number"
             # response = f"CON Please Confirm That this are Your  Details\nname:{name}\nphoneNumber:{phone}\nIdno:{id} \n1.Confirm\n2.Cancel"
          #  elif lastInput.isdigit() and lastInput !=1:
                response = "CON Dear You qualify For a loan of 5000-10000.Enter a loan Amount"


            elif lastInput.isdigit() and 10 <= int(lastInput) <= 15000:
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing which will be dispursed in 72hrs."
                stk_push_success(request)
            # elif (len(inputArray)==7 and lastInput == "1"):
            #     response = response = "END You Have Subscribe to 10 Mbs for Sh.1000 for 30days\n"
            # elif lastInput == "2" and len(inputArray) == 2:
            #     # Support contact request
            #     response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
        else:
            response = "END Check your input Details."
            stk_push_success(request)

        return HttpResponse(response,content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})

@csrf_exempt
@api_view(['GET', 'POST'])
def survey(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("MSISDN")
        INPUT = request.POST.get("ussd_string")
        print(INPUT)
        if Dialer.objects.filter(phone_number=MSISDN).exists():
            # There is already an entry with the same phone number, do something else
            pass
        else:
            # There is no entry with the same phone number, create a new Dialer instance and save it
            dialer = Dialer(phone_number=MSISDN)
            dialer.save()
        print(MSISDN)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]
        
            print(MSISDN)
            print(len(inputArray))
            
            if (lastInput == ''):
                response = {"response": "CON Welcome To Credit Checker\n1. Check Score\n2. Crb Status"}
                          
            elif (lastInput=='1' or lastInput=='2'):
                response = {"response": "CON Please Enter Your ID Number "}
            elif (len(inputArray)==3):
                response = {"response": "CON Please Enter Your Full Name"}
                # stk_push_success(request)
            elif (len(inputArray)==4):
                response = {"response": "CON Please Enter Your Email"}
     
            elif len(inputArray)==5:
                response = {"response": "END Please Proceed To pay And your scrore will be emailed to you."}
                # stk_push_success(request)
            elif lastInput == "3" and len(inputArray) == 2:
                response = {"response": "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."}
                # stk_push_success(request)
            else:
                response = {"response": "END You seem to have input wrong credentials. Please try again."}
        else:
            response = {"response": "Invalid input received."}
        
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Invalid request method. Please use Choose an Input."})



@csrf_exempt
@api_view(['GET', 'POST'])
def bundwer(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("MSISDN")
        INPUT = request.POST.get("ussd_string")
        print(INPUT)
        print(MSISDN)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]

            print(MSISDN)
            print(len(inputArray))

            if (lastInput == ''):
                response = "CON Welcome To Glownet.Select Language\n1. English\n2. Kiswahili"

            # elif (lastInput == '213'):
            #     response = "CON Welcome To Boon Finance\n1. Register\n2. Get a loan\n3. Buy Airtime\n4. Pay for Wi-fi Services"
            elif (lastInput=='1' or lastInput=='2'):
                response = "CON Please Enter Your ID Number "
            elif (lastInput.isdigit() and len(lastInput) >6):
                response = "CON Please Enter Your Full Name"
            elif lastInput.isalpha():
                response = "CON Please Select Gender\n3.Male\n4.Female "
            elif (lastInput=='3' or lastInput=='4'):
                # name = inputArray[1]
                #  ID = inputArray[0]
                # gender = inputArray[2]
                response = "CON Please Confirm That You Understand the terms And Conditions\n\n5.Confirm\n6.Cancel"
            elif(lastInput =='5'):
                response = "CON Welcome  to Glownet\n7.Get a loan\n8.Pay Loan\n9.contact us"
            elif (lastInput=='7'):
                response = "CON Enter loan amount between 1500-15000\n"
            elif (lastInput.isdigit() and len(lastInput) <6):
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing."
                stk_push_success(request)
            # elif lastInput == "3" and len(inputArray) == 2:
            #     response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
            #     stk_push_success(request)
            else:
                response = "END You have subscribed To Glownet Loans You will receive the service in 20 mins."
        else:
            response = "Invalid input received."

        return HttpResponse(response, content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})


@csrf_exempt
@api_view(['GET', 'POST'])
def score(request):
    if request.method == 'GET':
        global INPUT 
        global MSISDN
        SESSIONID = request.GET.get("session_id")
        USSDCODE = request.GET.get("service_code")
        MSISDN = request.GET.get("MSISDN")
        INPUT = request.GET.get("text")
        # inputArray = INPUT.split("*") # the last value after * is what the user entered last
        # lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this>
        # this is the entry point
        # print(MSISDN)
        # print(len(inputArray))
        # print(lastInput)
        # if Dialer.objects.filter(phone_number=MSISDN).exists():
        #    pass
        # else:
        #     # There is no entry with the same phone number, create a new Dialer instance and save it
        #     dialer = Dialer(phone_number=MSISDN)
        #     dialer.save()  
            # this is the entry point
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1]
            if (lastInput == ""):
                response = f"CON WELCOME TO HOMIKA PESA \n1. Apply Loan\n2. Buy Airtime\n3.Invite Friend\n4.My Account "
            # elif len(inputArray)==1:
            #     response = "CON Please Enter Your FullName "
                #response = f"CON Please confirm that this is your phone number {MSISDN}\n 5.Proceed "

            elif len(inputArray)==1:
                response = "CON Please Enter Your ID Number"
            elif len(inputArray)==2:
                response = "CON Select Loan Type \n1.30 Days loan\n2.90 Days Loan"
            elif len(inputArray)==3:
                response = "CON Your Loan Limit is 55000\n Enter Amount"

            elif len(inputArray)==4:
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
                stk_push_success(request)
                # response = "CON View loan options\n 9. Short-term loan: 5% interest, due in 30 days\n 10. Medium-term loan: 10% interest, due in 90 days\n"
                #print(inputArray[1])
            # elif (lastInput=='9' or lastInput=='10'):
            #     response = "CON Enter loan amount between 1000-15000\n"
            # elif lastInput.isdigit() and 1000 <= int(lastInput) <= 15000:
            #     response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
            #     stk_push_success(request)
            # elif lastInput == "3" and len(inputArray) == 2:
            #     response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx.",
            #     stk_push_success(request)
            else:
                response = "END This option has not been implemented yet. Please try again later."
                stk_push_success(request)
            return HttpResponse(response,content_type='text/plain')
        else:
            return HttpResponse({"error": "Invalid request method. Please use POST."})


