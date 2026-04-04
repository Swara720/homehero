from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('favorite/<int:service_id>/', views.toggle_favorite, name='toggle_favorite'),
]