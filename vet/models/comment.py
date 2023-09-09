from django.db import models
from django.contrib.auth import get_user_model


class VetComment(models.Model):
    vet = models.ForeignKey("accounts.VetProfile", on_delete=models.CASCADE, related_name="vet_comments")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="vet_comments")
    title = models.CharField(max_length=64)
    text = models.TextField()
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.vet) + ' | ' + str(self.title)



