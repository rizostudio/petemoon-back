from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from accounts.models.user import User
from vet.models import ReserveTimes


class VetProfile(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE, related_name="vet_profile" )
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    medical_number = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(null=True,blank=True)
    national_card_front = models.FileField(null=True, blank=True)
    national_card_back = models.FileField(null=True, blank=True)
    birth_certificate = models.FileField(null=True,blank=True)
    medical_card = models.FileField(null=True,blank=True)
    military_card = models.FileField(null=True,blank=True)
    gender = models.CharField(max_length=64, null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    expertise = models.CharField(max_length=255, null=True, blank=True)
    pet_type_experience = models.CharField(max_length=255, null=True, blank=True)
    pet_category_fav = models.CharField(max_length=255, null=True, blank=True)
    reserve_times = models.ManyToManyField(ReserveTimes,blank=True,related_name="vet_reserve_times")
    is_approved = models.BooleanField(default=False)
    about = models.TextField(null=True)
    price = models.IntegerField(default=200, null=True, blank=True)

    def __str__(self):
        if self.user:
            return self.user.phone_number
        else:
            return str(self.id)



    class Meta:
        verbose_name = "Vet Profile"
        verbose_name_plural = "Vet Profiles"
    
    @property
    def is_complete(self):
        return bool(
            self.gender
            and self.national_card_front
            and self.national_card_back
        )


@receiver(post_save, sender=User)
def create_petshop_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "vet":
        VetProfile.objects.create(user=instance)
