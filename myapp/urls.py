from django.urls import path
from .views import webhook_handler, index


from django.urls import include, path

urlpatterns = [
    path('webhook/', webhook_handler, name='webhook_handler'),
    path('', index, name='index'),
]
