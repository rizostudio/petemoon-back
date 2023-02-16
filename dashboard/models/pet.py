from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.choices import Choices


class PetType(models.Model):
    pet_type = models.CharField(max_length=256)

    class Meta:
        verbose_name = _("PetType")
        verbose_name_plural = _("PetTypes")

    def __str__(self):
        return self.pet_type


class PetCategory(models.Model):
    pet_category = models.CharField(max_length=256)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True, db_index=True, null=True)

    class Meta:
        verbose_name = _("PetCategory")
        verbose_name_plural = _("PetCategorys")

    def __str__(self):
        return self.pet_category


class Pet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, null=True)
    sex = models.CharField(choices=Choices.Sex.choices, max_length=1)
    pet_category = models.ForeignKey(
        PetCategory, on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(null=True)
    photo = models.ImageField(blank=True,null=True)
    # Medical
    weight = models.FloatField(null=True)
    last_vaccine_date = models.DateField(null=True)
    underlying_disease = models.CharField(max_length=128, null=True)
    last_anti_parasitic_vaccine_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")

    def __str__(self):
        return self.name
