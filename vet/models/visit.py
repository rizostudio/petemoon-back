from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model


class Visit(models.Model):
    vet = models.ForeignKey(
        "accounts.VetProfile", on_delete=models.CASCADE, related_name="visit"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="visit"
    )
    pet = models.ForeignKey("dashboard.Pet",on_delete=models.CASCADE,)
    explanation = models.TextField()
    reason = models.CharField(max_length=256)
    photo = models.ImageField(blank=True,null=True)