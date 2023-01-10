from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    title = models.CharField(max_length=64)
    text = models.TextField()
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
