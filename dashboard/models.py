from django.db import models
from utils.choices import Choices


class Pet(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    type = models.PositiveSmallIntegerField(choices=Choices.PetType.choices)
    sex = models.CharField(choices=Choices.Sex.choices,max_length=1)
    species = models.CharField(max_length=128)
    birth_date = models.DateField(null=True)

    #Medical
    weight = models.FloatField()
    last_vaccine_date = models.DateField()
    underlying_disease = models.CharField(max_length=128)
    last_anti_parasitic_vaccine_date = models.DateField()
