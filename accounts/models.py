from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('provider', 'Service Provider'),
        ('customer', 'Customer'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def is_provider(self):
        return self.user_type == 'provider'

    def is_customer(self):
        return self.user_type == 'customer'

    def __str__(self):
        return self.username