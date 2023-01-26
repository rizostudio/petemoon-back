from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models.user import User


class PetshopProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="petshop_profile"
    )
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    postal_region = models.CharField(max_length=64, null=True, blank=True)
    national_card = models.ImageField(null=True, blank=True)
    estimated_delivery_time = models.IntegerField(default=0)

    class Meta:
        verbose_name = "petshop profile"
        verbose_name_plural = "petshop profiles"




@receiver(post_save, sender=User)
def create_petshop_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "petshop":
        PetshopProfile.objects.create(user=instance)
