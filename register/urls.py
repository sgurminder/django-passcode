from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from views import Register
from views import verify_and_create

urlpatterns = patterns('',
                       url(r'^register/$',Register),
                       url(r'^verify/$', verify_and_create),
)
                       

