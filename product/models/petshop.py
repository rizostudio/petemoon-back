from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import PetshopProfile,User


class Petshop(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(
        "product.Product", through="product.ProductPricing"
    )
    slug = models.SlugField(unique=True, db_index=True, null=True)
    owner = models.OneToOneField(
        PetshopProfile,
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="shops",
    )

    @property
    def is_complete(self):
        return bool(self.name)
    
    @receiver(post_save, sender=PetshopProfile)
    def create_petshop_profile(sender, instance, created, **kwargs):
        if created :
            Petshop.objects.create(owner=instance)

    def __str__(self):
        return str(self.name)+' | '+str(self.owner)

