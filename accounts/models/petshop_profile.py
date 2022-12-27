from django.db import models

from accounts.models.user import User


class PetshopProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="petshop_profile"
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "petshop profile"
        verbose_name_plural = "petshop profiles"

    def __str__(self):
        return self.name
