# django-passcode
Django passcode is a project to enable mobile device registration and verification using SMS based passcode. It uses a simple user model with mobile number and device id pair as primary key. A unique token is generated for mobile number and device id pair. Requests from mobile device can be authorized based on generated token. Changes in device will force re registration using sms passcode.


#Requirments
  - Django Rest Framework(rest_framework) in INSTALLED_APPS in settings.py


#Installation

  - Include "register" in Installed apps of your project
  - Include (r'^signup/', include('register.urls')) in project urls.py


# Usage

API
===

1. Register : A POST request to <your_domain>/signup/register/

Post Parameters
   - mobile 
   - Device id

Response: JSON response 

