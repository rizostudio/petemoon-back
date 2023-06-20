from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from accounts.models.user import User


class PetshopProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="petshop_profile"
    )
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    postal_region = models.CharField(max_length=64, null=True, blank=True)
    national_id_validator = RegexValidator(
        r"^(\d{10})?$", message=_("Invalid national ID.")
    )
    national_id = models.CharField(
        max_length=10,
        validators=[national_id_validator],
        null=True,
        blank=True,
    )
    #files
    national_card = models.FileField(null=True, blank=True)
    birth_certificate = models.FileField(null=True, blank=True)
    business_license = models.FileField(null=True, blank=True)
    union_license = models.FileField(null=True, blank=True)
    tax_certificate = models.FileField(null=True, blank=True)

    estimated_item_count = models.IntegerField(default=0)
    gender = models.CharField(max_length=64, null=True, blank=True)
    sheba_number_validator = RegexValidator(
        r"^(IR\d{24})?$", message=_("Invalid sheba.")
    )
    sheba_number = models.CharField(
        max_length=26,
        validators=[sheba_number_validator],
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "petshop profile"
        verbose_name_plural = "petshop profiles"

    @property
    def is_complete(self):
        return bool(
            self.address
            and self.gender
            and self.national_id
            and self.national_card
            and self.city
            and self.postal_region
            and self.estimated_item_count
        )
    
    def __str__(self):
        return f"{self.first_name + self.last_name}"


@receiver(post_save, sender=User)
def create_petshop_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "petshop":
        PetshopProfile.objects.create(user=instance)
