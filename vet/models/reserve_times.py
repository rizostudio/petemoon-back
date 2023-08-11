from django.db import models
from datetime import datetime


class ReserveTimes(models.Model):
    vet = models.ForeignKey("accounts.VetProfile", on_delete=models.CASCADE, related_name="vet_reserve", null=True)
    time = models.DateTimeField()
    availabe = models.BooleanField(default=True)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vet.user.first_name)+' '+str(self.vet.user.last_name) +' | '+ str(self.time)
