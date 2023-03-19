from django.db import models
from datetime import datetime


class ReserveTimes(models.Model):
    time = models.DateTimeField()