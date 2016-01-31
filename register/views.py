# Create your views here.

from models import UserBase
from models import PasscodeVerify

from django.http import HttpResponse
from django.views.generic import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


import random
import binascii
import os
import re

@csrf_exempt
@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        
        response_data = {'code' : 'Invalid Data' }
        
        #Raise exception in case bad data
        try:
            mobile = request.POST['mobile']
            device_id = request.POST['device_id']
            
        except:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        validate = re.search('^[789]\d{9}$', mobile)
        if validate is None:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            #check user already
        try:
            user = UserBase.objects.get(mobile = mobile, device_ident = device_id)
        except UserBase.DoesNotExist:
            user = ''
        
        if user:
            user.token = ''
            response_data['code'] = 'Re-Registering'
            user.is_verified =  False
            user.save()
            
            #create passcode and send response
        pl = random.sample([1,2,3,4,5,6,7,8,9,0],4)
        passcode = ''.join(str(p) for p in pl)

        try:
            #create entry in passcode table for verification
            passcode_entry, created = PasscodeVerify.objects.update_or_create(mobile=mobile,  defaults={'device_ident' : device_id, 'passcode' : passcode,'is_verified' : False})

        except:
            response_data['is_verified']  = "Expire"
            return Response(response_data, status = status.HTTP_400_BAD_REQUEST)
        response_data['passcode'] = passcode
        response_data['code'] = 'Success'
            
            # SMS api to send passcode
        return Response(response_data, status = status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
def verify_and_create(request):
    #verify passcode in PasscodeVerify table
    response_data = {'code' : 'Invalid Data' }
    if request.method == 'POST':
        try:
            mobile = request.POST['mobile']
            device_id = request.POST['device_id']
            passcode = request.POST['passcode']
        except:
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)

        try:
            valid = PasscodeVerify.objects.get(mobile = mobile, device_ident = device_id , passcode = passcode, is_verified = False)
        except PasscodeVerify.DoesNotExist:
            response_data['code'] = 'Invalid/Expired passcode'
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)

        if valid:
            valid.is_verified = True
            valid.save()


        #Generate token 
        token = binascii.hexlify(os.urandom(20)).decode()
        created = ''
        #update or create user device_id and token
        try:
            user,created = UserBase.objects.update_or_create(mobile = mobile,  defaults = {'device_ident' : device_id , 'token' : token ,'is_active' : True})
        except:
            response_data['code'] = 'User creation error'
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)

        response_data['code'] = 'Success User created'
        response_data['token'] = token

        return Response(response_data,status=status.HTTP_201_CREATED)

#Done
#Re-register request authorization


# Next : SMS API integration, 
#validate mobile number format in Post
#Token as one to one field user
#Encrypt device-ident
#Format code for Github and upload
