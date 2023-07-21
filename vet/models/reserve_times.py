from django.db import models
from datetime import datetime


class ReserveTimes(models.Model):
    vet = models.ForeignKey("accounts.VetProfile", on_delete=models.CASCADE, related_name="vet_reserve")
    time = models.DateTimeField()
    availabe = models.BooleanField(default=True)
    reserved = models.BooleanField(default=False)