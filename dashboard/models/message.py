from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    context = models.TextField()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")