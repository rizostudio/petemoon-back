from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _



class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    context = models.TextField()
    title = models.CharField(max_length=256,null=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title) +' | '+ str(self.user)


    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")