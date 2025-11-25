from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django_countries.fields import CountryField

# Create your models here.

class AddressField(models.Model):
    """
    AddressField Model to store user address information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    state = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)

    def __str__(self):
        return f'{self.user.username} Address'

class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_address = models.OneToOneField(AddressField, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """             
    if created:
        UserProfile.objects.create(user=instance)     
    # Existing users: just save the profile
    address = AddressField.objects.filter(user=instance).first()
    if not address:
        address = AddressField.objects.create(user=instance)
    instance.userprofile.default_address = address
    instance.userprofile.save()

