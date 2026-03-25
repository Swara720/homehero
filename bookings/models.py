from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from services.models import Service

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user} - {self.service}"