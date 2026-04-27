from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, ProviderProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'customer':
            CustomerProfile.objects.create(user=instance)
        elif instance.user_type == 'provider':
            ProviderProfile.objects.create(user=instance)