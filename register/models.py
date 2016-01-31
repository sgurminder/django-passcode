from django.db import models

class PasscodeVerify(models.Model):
    mobile = models.IntegerField(primary_key=True)
    device_ident = models.CharField(max_length = 20)
    passcode = models.CharField(max_length = 4,default='0000')
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return (str(self.mobile) + ',' + self.passcode)
   
class UserBaseManager(models.Manager):
    def get_by_natural_key(self,mobile):
        return self.get(mobile = mobile)


class UserBase(models.Model):
    mobile = models.IntegerField(primary_key=True)
    device_ident = models.CharField(max_length = 50)
    created_on = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length = 50,default = 'xyz')
    is_active = models.BooleanField(default = False)
    is_vendor = models.BooleanField(default=False)
    
    REQUIRED_FIELDS =['email']
    USERNAME_FIELD = 'mobile'

    def is_active_user(self):
        return self.is_active

    def is_vendor(self):
        return self.is_vendor

    def __str__(self):
        return self.mobile
    
