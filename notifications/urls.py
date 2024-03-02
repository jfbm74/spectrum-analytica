from django.urls import path
from . import views


urlpatterns = [
    path('wstest/', views.ws_test, name='ws_test'),
    path('smstest/', views.sms_test, name='sms_test'),
]