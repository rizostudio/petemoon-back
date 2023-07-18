from django.db import models
from django.contrib.auth import get_user_model

from shopping_cart.utils import random_N_chars_str
from utils.choices import Choices
from .reserve_times import ReserveTimes


class Visit(models.Model):
    vet = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="visit_vet")
    visit_id = models.CharField(max_length=128,unique=True,editable=False,null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="visit_user" )
    pet = models.ForeignKey("dashboard.Pet",on_delete=models.CASCADE,)
    explanation = models.TextField()
    reason = models.CharField(max_length=256)
    photo = models.ImageField(blank=True,null=True)
    time = models.ForeignKey(ReserveTimes,on_delete=models.CASCADE, null=True )
    prescription_summary = models.CharField(max_length=256,null=True,blank=True)
    prescription = models.TextField(blank=True)
    prescription_photo = models.ImageField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status = models.CharField(choices=Choices.Visit.choices, max_length=128, null=True,blank=True)
    def save(self):
        self.visit_id = default=random_N_chars_str(12)          
        super(Visit, self).save()
