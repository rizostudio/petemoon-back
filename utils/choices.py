from django.db import models
from django.utils.translation import gettext_lazy as _


class Choices(object):
    class PetType(models.IntegerChoices):
        DOG = 1, _("Dog")
        CAT = 1, _("Cat")
        BIRD = 1, _("Bird")
    
    class Sex(models.CharField):
        MALE = "M",_("Male")
        FEMALE = "F",_("Female")


    