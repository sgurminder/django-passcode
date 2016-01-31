from django.contrib import admin

from .models import UserBase,PasscodeVerify

admin.site.register(UserBase)
admin.site.register(PasscodeVerify)
