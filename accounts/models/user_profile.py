from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models.user import User
from dashboard.models import Wallet

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    birth_date = models.DateField(blank=True, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    referal_code = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return self.user.phone_number


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
