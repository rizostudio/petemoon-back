from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models.user import User


class PetshopProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="petshop_profile"
    )
    address = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    postal_region = models.CharField(max_length=64, null=True, blank=True)
    national_card = models.ImageField(null=True, blank=True)
    estimated_item_count = models.IntegerField(default=0)
    gender = models.CharField(max_length=64, null=True, blank=True)
    sheba_number_validator = RegexValidator(r"^(IR\d{24})?$")
    sheba_number = models.CharField(
        max_length=26,
        validators=[sheba_number_validator],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "petshop profile"
        verbose_name_plural = "petshop profiles"

    def __str__(self):
        return self.name

    @property
    def is_complete(self):
        return bool(
            self.address
            and self.gender
            and self.national_card
            and self.city
            and self.postal_region
            and self.estimated_item_count
        )


@receiver(post_save, sender=User)
def create_petshop_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "petshop":
        PetshopProfile.objects.create(user=instance)
