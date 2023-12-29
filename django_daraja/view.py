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
def bd(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("mobile_number")
        INPUT = request.POST.get("message")
        print(INPUT)
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
    
            # print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
                response = "CON Welcome To Credit Score Checker\n1. Request Credit Score\n2. Check If BlackListed" # note the NEW LINE \n
        
                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33

            elif lastInput == "1" and len(inputArray)==1:
                # Register option
                # Input validation and business logic can go here
                response = "CON Please Enter Your Full Name"

            elif (len(inputArray) == 2):
                response = "CON Please Enter Your Phone Number "
            elif (len(inputArray) ==3):
                response = "Enter Your Id Number"
            elif (len(inputArray) ==4):
                response = "CON INput Your Email Address"
            # elif (len(inputArray) ==5):
            #     response = "CON Number of Devices Allowed\n1. Two Devices\n2. Five Devices"

            # elif (len(inputArray)==6 and lastInput== "1"):
            #     response = "CON Available products Two Devices\n1. 5 Mbs @500 per Month\n2. 10 Mbs @1000 per Month\n3. 20 Mbs @1500 per Month\n4. 50 Mbs @2500 per Month"
            # elif (len(inputArray)==7 and lastInput == "1"):
            #     response = response = "END You Have Subscribe to 10 Mbs for Sh.1000 for 30days\n"
            elif lastInput == "2" and len(inputArray) == 2:
                # Support contact request
                response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
        else:
            response = "END You will receive a Credit Report  in your email soon."
        
        return HttpResponse(response,content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})

@csrf_exempt
@api_view(['GET', 'POST'])
def bnd(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("mobile_number")
        INPUT = request.POST.get("message")
        print(INPUT)
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
    
            # print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
                response = "CON Welcome To  PROFITKA VENTURES\n1. English\n2. Kiswahili" # note the NEW LINE \n
        
                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33

            elif ((lastInput == "1" and len(inputArray)==1)or(lastInput == "2" and len(inputArray)==1)):
                # Register option
                # Input validation and business logic can go here
                response = "CON Please Enter Your Full Name"

            elif (len(inputArray) == 2):
                response = "CON Please Enter Your Phone Number "
            elif (len(inputArray) ==3):
                response = "Enter Your Id Number"
            elif (len(inputArray) ==4):
                name=inputArray[1]
                phone=inputArray[2]
                id=inputArray[3]
                response = f"Please Confirm That this are Your  Details\nname:{name}\nphoneNumber:{phone}\nIdno:{id} \n1.Confirm\n2.Cancel"
            elif (len(inputArray) ==5):
                name=inputArray[1]
                response = f"CON Dear {name} You qualify For a loan of 5000-10000.Enter a loan Amount"

            elif (len(inputArray)==6):
                response = "Please Deposit a Refundable Security fee for Your Loan Processing which will be dispursed in 20mins."
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
# def bund(request):
#     if request.method == 'POST':
#         global INPUT 
#         global lastInput
#         lastInput = ''
#         SESSIONID = request.POST.get("session_id")
#         USSDCODE = request.POST.get("service_code")
#         MSISDN = request.POST.get("mobile_number")
#         INPUT = request.POST.get("message")
#         print(INPUT)
#         if INPUT is not None:
#             inputArray = INPUT.split("*") # the last value after * is what the user entered last
#             lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
#         # this is the entry point
    
#             print(MSISDN)
#             print(len(inputArray))
    
#             # this is the entry point
#             if (lastInput == ""):
#                 response = "CON Welcome To Glownet Wi-Fi Solutions\n1. Register as a new Member\n2. Subscribe To one of Our products" # note the NEW LINE \n
        
#                 #inputArray = INPUT.split("*") # the last value after * is what the user entered last
#                 #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33

#             elif lastInput == "1" and len(inputArray)==1:
#                 # Register option
#                 # Input validation and business logic can go here
#                 response = "CON Please Enter Your Full Name"

#             elif (len(inputArray) == 2):
#                 response = "CON Please Enter Your Phone Number "
#             elif (len(inputArray) ==3):
#                 response = "Create New Password "
#             elif (len(inputArray) ==4):
#                 response = "CON Please Input Town"
#             elif (len(inputArray) ==5):
#                 response = "CON Number of Devices Allowed\n1. Two Devices\n2. Five Devices"

#             elif (len(inputArray)==6 and lastInput== "1"):
#                 response = "CON Available products Two Devices\n1. 5 Mbs @500 per Month\n2. 10 Mbs @1000 per Month\n3. 20 Mbs @1500 per Month\n4. 50 Mbs @2500 per Month"
#             elif (len(inputArray)==7 and lastInput == "1"):
#                 response = response = "END You Have Subscribe to 10 Mbs for Sh.1000 for 30days\n"
#             elif lastInput == "2" and len(inputArray) == 2:
#                 # Support contact request
#                 response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
#         else:
#             response = "END You have subscribed To Glownet Wifi Services You will be able to use the service in 20 mins."
        
#         return HttpResponse(response,content_type='text/plain')
#     else:
#         return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})

def bnd(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        lastInput = ''
        SESSIONID = request.POST.get("session_id")
        USSDCODE = request.POST.get("service_code")
        MSISDN = request.POST.get("mobile_number")
        INPUT = request.body.decode('utf-8')  # get the raw request body as plain text
        print(INPUT)
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
    
            print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
                response = "CON Welcome To Glownet Wi-Fi Solutions\n1. Register as a new Member\n2. Subscribe To one of Our products" # note the NEW LINE \n
        
                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33

            elif lastInput == "1" and len(inputArray)==1:
                # Register option
                # Input validation and business logic can go here
                response = "CON Please Enter Your Full Name"

            elif (len(inputArray) == 2):
                response = "CON Please Enter Your Phone Number "
            elif (len(inputArray) ==3):
                response = "Create New Password "
            elif (len(inputArray) ==4):
                response = "CON Please Input Town"
            elif (len(inputArray) ==5):
                response = "CON Number of Devices Allowed\n1. Two Devices\n2. Five Devices"

            elif (len(inputArray)==6 and lastInput== "1"):
                response = "CON Available products Two Devices\n1. 5 Mbs @500 per Month\n2. 10 Mbs @1000 per Month\n3. 20 Mbs @1500 per Month\n4. 50 Mbs @2500 per Month"
            elif (len(inputArray)==7 and lastInput == "1"):
                response = response = "END You Have Subscribe to 10 Mbs for Sh.1000 for 30days\n"
            elif lastInput == "2" and len(inputArray) == 2:
                # Support contact request
                response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
        else:
            response = "END You have subscribed To Glownet Wifi Services You will be able to use the service in 20 mins."
        
        return HttpResponse(response, content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."}, content_type='application/json')


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

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
        MSISDN = request.POST.get("mobile_number")
        INPUT = request.POST.get("message")

        print(INPUT)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]
            if lastInput == '':
                response = "CON Welcome to Chest Survey\n1. Enter your name\n"
            elif len(inputArray) == 1:
                response = "CON What is your age?\n"
            elif len(inputArray) == 2:
                response = "CON What is your gender?\n1. Male\n2. Female\n3. Other\n"
            elif len(inputArray) == 3:
                response = "CON What is you Average Income"
            elif len(inputArray) == 4:
                response = "CON What is your occupation?\n1. Student\n2. Employed\n3. Self-employed\n4. Unemployed\n"
            elif len(inputArray) == 5:
                response = "CON Thank you for taking our survey. Do you have any feedback for us?\n"
            elif len(inputArray) == 6:
                response = "END Thank you for your feedback. Have a great day!"
            else:
                response = "Invalid input received."
        else:
            response = "Invalid input received."
        return HttpResponse(response, content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})


@csrf_exempt
@api_view(['GET', 'POST'])
def Index(request):
    if request.method == 'GET':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("sessionID")
        USSDCODE = request.POST.get("")
        serviCode = request.POST.get("")
        MSISDN = request.POST.get("MSISDN")
        INPUT = request.POST.get("text")
        print(INPUT)
        print(MSISDN)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]
        
            print(MSISDN)
            print(len(inputArray))
            
            if (lastInput == ''):
                response = "CON Main menu\n1. Register\n2. Get a loan\n3. Buy Airtime\n"
            
            elif (lastInput == '54'):
                response = "CON Main menu\n1. Register\n2. Get a loan\n3. Buy Airtime\n"                
            elif lastInput == "1" and len(inputArray)==1:
                response = "CON Please Enter Your ID Number "

            elif (len(inputArray) == 2):
                response = "CON Please Enter Your Phone Number "
            elif (len(inputArray) ==3):
                response = "CON Loan Options\n1. View loan Limit\n2. Apply for a loan\n"
            elif ((len(inputArray) ==4) and lastInput=="1"):
                response = "CON Your Loan Limit is 15000\n1.Proceed"
                print(inputArray[3])
            elif ((len(inputArray) ==5 and inputArray[3]=='1') or (len(inputArray)==4 and lastInput=='2')):
                response = "CON View loan options\n1. Short-term loan: 5% interest, due in 30 days\n2. Medium-term loan: 10% interest, due in 90 days\n3. Long-term loan: 15% interest, due in 180 days\n"
                #print(inputArray[1])
            elif ((len(inputArray)==6 and inputArray[4]=='1') or (inputArray[3]=='2' and len(inputArray)==5)):
                response = "CON Enter loan amount\n"
            elif (len(inputArray)==7 or (len(inputArray)==6 and inputArray[3]=='2')):
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing."
                stk_push_success(request)
            elif lastInput == "2" and len(inputArray) == 2:
                response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
                stk_push_success(request)
            else:
                response = "END You have subscribed To Glownet Loans You will receive the service in 20 mins."
        else:
            response = "Invalid input received."
        
        return HttpResponse(response, content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})

@csrf_exempt
@api_view(['GET', 'POST'])
def scored(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("sessionID")
        USSDCODE = request.POST.get("accessPoint")
        MSISDN = request.POST.get("MSISDN")
        INPUT = request.POST.get("text")
        print(INPUT)
        print(MSISDN)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]
        
            print(MSISDN)
            print(len(inputArray))
            
            if (lastInput == '34'):
                response = "CON Welcome To Credit Checker\n1. Check Score\n2. Crb Status"
                          
            elif (lastInput=='1' or lastInput=='2'):
                response = "CON Please Enter Your ID Number "
            elif (len(inputArray)==3):
                response = "CON Please Enter Your Full Name"
                # stk_push_success(request)
            elif (len(inputArray)==4):
                response = "CON Please Enter Your Email"
            # elif (lastInput=='3' or lastInput=='4'):
            #     name = inputArray[1]
            #     ID = inputArray[0]
            #     gender = inputArray[2]
            #     response = f"CON Please Confirm That You are\nname:{name}\nID No:{ID}\nGender:{gender}\n\n5.Confirm\n6.Cancel"
            # elif(lastInput =='3' or lastInput == '4'):
            #     name = inputArray[1]
            #     response = f"CON Welcome to Glownet\n7.Get a loan\n"
            # elif (lastInput=='7'):
            #     response = "CON Enter loan amount between 4500-15000\n"
            elif len(inputArray)==5:
                response = "END Please Proceed To pay And your scrore will be emailed to you."
                stk_push_success(request)
            elif lastInput == "3" and len(inputArray) == 2:
                response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
                stk_push_success(request)
            else:
                response = "END You seem to have input wrong credetials in Try again."
        else:
            response = "Invalid input received."
        
        return HttpResponse(response, content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use Choose an Input."})

@csrf_exempt
@api_view(['GET', 'POST'])
def scored(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        data = json.loads(request.body.decode('utf-8'))
        SESSIONID = data.get("session_id")
        USSDCODE = data.get("service_code")
        MSISDN = data.get("MSISDN")
        INPUT = data.get("ussd_string")
        print(INPUT)
        print(MSISDN)
        if INPUT is not None:
            inputArray = INPUT.split("*")
            lastInput = inputArray[len(inputArray) - 1]
        
            print(MSISDN)
            print(len(inputArray))
            
            if (lastInput == '34'):
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
                stk_push_success(request)
            elif lastInput == "3" and len(inputArray) == 2:
                response = {"response": "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."}
                stk_push_success(request)
            else:
                response = {"response": "END You seem to have input wrong credetials in Try again."}
        else:
            response = {"response": "Invalid input received."}
        
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Invalid request method. Please use Choose an Input."})


@csrf_exempt
@api_view(['GET', 'POST'])
def bund(request):
    if request.method == 'GET':
        global INPUT 
        global MSISDN
        SESSIONID = request.GET.get("session_id")
        USSDCODE = request.GET.get("service_code")
        MSISDN = request.GET.get("mobile_number")
        INPUT = request.GET.get("message")
        inputArray = INPUT.split("*") # the last value after * is what the user entered last
        lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
        print(MSISDN)
        print(len(inputArray))
        print(lastInput)
    
            # this is the entry point
        if (lastInput == ""):
            response = f"CON WELCOME TO Acorn Finance \n1. Apply Loan\n2. Buy Airtime\n3.Invite Friend\n4.My Account "
        # elif len(inputArray)==1:
        #     response = "CON Please Enter Your FullName "
            #response = f"CON Please confirm that this is your phone number {MSISDN}\n 5.Proceed "

        elif len(inputArray)==1:
            response = "CON Please Enter Your ID Number"
        elif len(inputArray)==2:
            response = "CON Select Loan Type \n1.30 Days loan\n2.90 Days Loan"
        elif (lastInput =='1') and (len(inputArray) == 4) or (lastInput =='2') and (len(inputArray) == 4):
            response = "CON Your Loan Limit is 55000\n Enter Amount"
            
        elif len(inputArray)==3:
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
@api_view(['GET', 'POST'])
def bund(request):
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
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the sha>
        # this is the entry point
    
            # print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
               # response = "CON Welcome To  PROFITKA VENTURES\n1. English\n2. Kiswahili" # note the NEW LINE \n

                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of th>

           # elif ((lastInput == "1" and len(inputArray)==1)or(lastInput == "2" and len(inputArray)==1)):
                # Register option
                # Input validation and business logic can go here
              #  response = "CON Please Enter Your Full Name"
    # elif (len(inputArray) == 2):
            #    response = "CON Please Enter Your Phone Number "
           # elif (len(inputArray) == 3):
                response = "CON Enter Your Id Number"

           # elif (len(inputArray) == 4):
               # name=inputArray[1]
              #  phone=inputArray[2]
             #   id=inputArray[3]
            #    response = f"CON Please Confirm That this are Your  Details\nname:{name}\nphoneNumber:{phone}\nIdno:{id} \n1.Conf>
            elif len(lastInput) >6:
               # name=inputArray[1]
                response = "CON Dear  You qualify For a loan of 5000-10000.Enter a loan Amount"

            elif (len(lastInput) <6):
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing which will be dispursed in 72hrs"
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
def bnd(request):
    if request.method == 'GET':
        global INPUT 
        global MSISDN
        SESSIONID = request.GET.get("session_id")
        USSDCODE = request.GET.get("service_code")
        MSISDN = request.GET.get("mobile_number")
        INPUT = request.GET.get("message")
        inputArray = INPUT.split("*") # the last value after * is what the user entered last
        lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
        print(MSISDN)
        print(len(inputArray))
        print(lastInput)
    
            # this is the entry point
        if (lastInput == "36"):
            response = f"CON WELCOME TO HOMIKA FIRM \n1. Register\n2. Get a loan\n3. Buy Airtime\n4.Pay For wi-fi Services "
        elif (lastInput == "1")  or (lastInput == "2" ):
            response = "CON Please Enter Your Full Name "
            # response = f"CON Please confirm that this is your phone number {MSISDN}\n 5.Proceed "

        elif (lastInput.isalpha()):
            response = "CON Please Enter Your ID Number"
        elif (lastInput.isdigit() and len(lastInput)<10):
            response = "CON Please Enter Your Phone Number"
        elif (lastInput.isdigit() and len(lastInput)>=10):
            response = "CON Please Enter Your email Addess"
            
        elif "@" in lastInput:
            response = "END You will receive a message and An email with your report"
        # elif (lastInput=='9' or lastInput=='10'):
        #     response = "CON Please Enter Your Confirm Your Password"
        # elif lastInput.isdigit() and 1000 <= int(lastInput) <= 15000:
        #     response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
        #     stk_push_success(request)
        elif lastInput == "3" and len(inputArray) == 2:
            response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx.",
            # stk_push_success(request)
        else:
            response = "END This option has not been implemented yet. Please try again later."
        
        return HttpResponse(response,content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use POST."})
    
@csrf_exempt
@api_view(['GET', 'POST'])
def Airtime(request):
    if request.method == 'GET':
        global INPUT 
        global MSISDN
        SESSIONID = request.GET.get("session_id")
        USSDCODE = request.GET.get("service_code")
        MSISDN = request.GET.get("MSISDN")
        INPUT = request.GET.get("text")
        inputArray = INPUT.split("*") # the last value after * is what the user entered last
        lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
        print(MSISDN)
        print(len(inputArray))
        print(lastInput)
    
            # this is the entry point
        if (lastInput == ""):
            response = f"CON WELCOME TO Asamoah Airtime And Bundles Resellers\n1. Buy Airtime\n2. Buy Bundle\n"
        elif (lastInput == "1")  or (lastInput == "2" ):
            response = "CON Buy Airtime\n1. Buy For Self\n2. Buy for A friend "
            # response = f"CON Please confirm that this is your phone number {MSISDN}\n 5.Proceed "

        elif (lastInput.isalpha()):
            response = "CON Please Enter Your ID Number"
        elif (lastInput.isdigit() and len(lastInput)<10):
            response = "CON Please Enter Your Phone Number"
        elif (lastInput.isdigit() and len(lastInput)>=10):
            response = "CON Please Enter Your email Addess"
            
        elif "@" in lastInput:
            response = "END You will receive a message and An email with your report"
        # elif (lastInput=='9' or lastInput=='10'):
        #     response = "CON Please Enter Your Confirm Your Password"
        # elif lastInput.isdigit() and 1000 <= int(lastInput) <= 15000:
        #     response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
        #     stk_push_success(request)
        elif lastInput == "3" and len(inputArray) == 2:
            response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx.",
            # stk_push_success(request)
        else:
            response = "END This option has not been implemented yet. Please try again later."
        
        return HttpResponse(response,content_type='text/plain')
    else:
        return HttpResponse({"error": "Invalid request method. Please use POST."})


@csrf_exempt
@api_view(['GET', 'POST'])
def bund(request):
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
        if INPUT is not None:
            inputArray = INPUT.split("*") # the last value after * is what the user entered last
            lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33
        # this is the entry point
    
            # print(MSISDN)
            print(len(inputArray))
    
            # this is the entry point
            if (lastInput == ""):
                response ="CON Welcome To  PROFITKA VENTURES\n1. English\n2. Kiswahili" # note the NEW LINE \n

                #inputArray = INPUT.split("*") # the last value after * is what the user entered last
                #lastInput = inputArray[len(inputArray) - 1] # if on a shared ussd, the initial input will be the identifier of the shared code. e.g *415*33# .. this input will be 33

            elif ((lastInput == "1" and len(inputArray)==1)or(lastInput == "2" and len(inputArray)==1)):
                # Register option
                # Input validation and business logic can go here
                response ="CON Please  Enter Your Full Name"

           # elif (lastInput.isalpha()):
           #     response = "CON Please Enter Your Phone Number "
            elif lastInput.isalpha():
                response = "CON Enter Your Id Number"
             # response = f"CON Please Confirm That this are Your  Details\nname:{name}\nphoneNumber:{phone}\nIdno:{id} \n1.Confirm\n2.Cancel"
            elif lastInput.isdigit() and len(lastInput) > 6:
                response = "CON Dear You qualify For a loan of 5000-10000.Enter a loan Amount"


            elif len(lastInput)>2:
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing which will be dispursed in 20mins."
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
@csrf_exempt
@api_view(['GET', 'POST'])
def score(request):
    if request.method == 'POST':
        global ID_NUMBER, LOAN_AMOUNT
        ID_NUMBER = ''
        LOAN_AMOUNT = ''
        # retrieve user input
        session_id = request.POST.get("session_id")
        ussd_code = request.POST.get("service_code")
        msisdn = request.POST.get("msisdn")
        input_str = request.POST.get("message")
        last_input = input_str.split("*")[-1].strip()
        
        # initialize response
        response = ""
        
        # check current step and update variables accordingly
        if last_input == "":
            response = "CON Welcome TO Homika Finances.\n1.30 days Loan\n2.90 days Loan"
                                
        elif last_input == "1" or last_input == "2":
            response = "CON Please Input Your ID Number"
        elif last_input.isdigit() and len(last_input) >4:
            ID_NUMBER = last_input
            response = "CON Your Loan Limit is 15000\nEnter Loan Amount"
        elif ID_NUMBER and last_input.isdigit():
            LOAN_AMOUNT = last_input
            response = "END Please Deposit a Refundable Security fee for Your Loan Processing."
            stk_push_success(request)
        else:
            response = "END This option has not been implemented yet. Please try again later."
            
        # save response to session
        # if session_id:
        #     request.session[session_id] = response
            
        # return response
        return HttpResponse(response, content_type='text/plain')
        
    else:
        return HttpResponse({"error": "Invalid request method. Please use POST."})



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


@csrf_exempt
@api_view(['GET', 'POST'])
def bund(request):
    if request.method == 'POST':
        global INPUT 
        global lastInput
        global MSISDN
        lastInput = ''
        SESSIONID = request.POST.get("sessionID")
        USSDCODE = request.POST.get("accessPoint")
        MSISDN = request.POST.get("msisdn")
        INPUT = request.POST.get("message")
        print(INPUT)
        print(MSISDN)
        if Dialer.objects.filter(phone_number=MSISDN).exists():
            # There is already an entry with the same phone number, do something else
            pass
        else:
            # There is no entry with the same phone number, create a new Dialer instance and save it
            dialer = Dialer(phone_number=MSISDN)
            dialer.save()
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
            elif len(lastInput) >5:
               # response = "CON Please Enter Your Full Name"
              #  stk_push_success(request)
 #elif lastInput.isalpha():
             #   response = "CON Please Select Gender\n3.Male\n4.Female "
            # elif (lastInput=='3' or lastInput=='4'):
            #     name = inputArray[1]
            #     ID = inputArray[0]
            #     gender = inputArray[2]
            #     response = f"CON Please Confirm That You are\nname:{name}\nID No:{ID}\nGender:{gender}\n\n5.Confirm\n6.Cancel"
            #elif(lastInput =='3' or lastInput == '4'):
               # name = inputArray[1]
               # response = f"CON Welcome to Glownet\n7.Get a loan\n"
           # elif (lastInput=='7'):
                response = "CON Enter loan amount between 500-15000\n"
            elif lastInput.isdigit():
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing."
                stk_push_success(request)
            elif lastInput == "3" and len(inputArray) == 2:
                response = "END Contact our support on the following numbers 2547xxxxxxx, 25402xxxxx."
                stk_push_success(request)
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
           # elif len(inputArray)==2:
            #    response = "CON Select Loan Type \n1.30 Days loan\n2.90 Days Loan"
            elif len(inputArray)==2:
                response = "CON Your Loan Limit is 55000\n Enter Amount"

            elif len(inputArray)==3:
                response = "END Please Deposit a Refundable Security fee for Your Loan Processing.\n",
                stk_push_success(request)

            else:
                response = "END This option has not been implemented yet. Please try again later."
                stk_push_success(request)
            return HttpResponse(response,content_type='text/plain')
        else:
            return HttpResponse({"error": "Invalid request method. Please use POST."})
