from django.urls import path
from .views import webhook_handler, pull_request_list

from django.urls import include, path

urlpatterns = [
    path('webhook/', webhook_handler, name='webhook_handler'),
    path('', pull_request_list, name='pull_requests'),
]
