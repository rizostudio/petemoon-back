from django.db import models
from django.utils.translation import gettext_lazy as _


class Choices(object):
    class PetType(models.IntegerChoices):
        DOG = 1, _("Dog")
        CAT = 2, _("Cat")
        BIRD = 3, _("Bird")
    
    class Sex(models.TextChoices):
        MALE = "M",_("Male")
        FEMALE = "F",_("Female")


    