from django.urls import path
from .views import create_service, service_list

urlpatterns = [
    path('', service_list, name='service_list'),
    path('create/', create_service, name='create_service'),
]