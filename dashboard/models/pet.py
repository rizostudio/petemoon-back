from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.choices import Choices
from django.contrib.auth import get_user_model


class Pet(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    type = models.PositiveSmallIntegerField(choices=Choices.PetType.choices)
    sex = models.CharField(choices=Choices.Sex.choices,max_length=1)
    species = models.CharField(max_length=128)
    birth_date = models.DateField(null=True)
    photo = models.ImageField()
    
    #Medical
    weight = models.FloatField()
    last_vaccine_date = models.DateField(null=True)
    underlying_disease = models.CharField(max_length=128,null=True)
    last_anti_parasitic_vaccine_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")

    def __str__(self):
        return self.name

