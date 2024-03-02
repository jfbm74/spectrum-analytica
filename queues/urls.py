from django.urls import path
from . import views


urlpatterns = [
    path('', views.active_queues, name='queues'),
]