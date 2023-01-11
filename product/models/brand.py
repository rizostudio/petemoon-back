from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name
