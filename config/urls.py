from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import admin_dashboard

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    
    # path('admin/', admin.site.urls),
    
    # Services & Home
    path('', include('services.urls')),
    
    # Accounts (login, register, logout)
    path('accounts/', include('accounts.urls')),
    
    # Bookings
    path('bookings/', include('bookings.urls')),
    
    # Payments
    path('payments/', include('payments.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)