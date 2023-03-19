from django.db import models

class ReserveTimes(models.Model):
    time = models.DateTimeField()