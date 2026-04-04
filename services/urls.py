from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.service_list, name='service_list'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/create-service/', views.create_service, name='create_service'),
    path('service/<int:service_id>/review/', views.add_review, name='add_review'),
]