from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models.user_manager import UserManager


class User(AbstractUser):
    username = None
    phone_regex = RegexValidator(
        regex=r"^09\d{9}",
        message="{}\n{}".format(
            _("Phone number must be entered in the format: '09999999999'."),
            _("Up to 11 digits allowed."),
        ),
    )
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        validators=[phone_regex],
        max_length=11,
        blank=False,
        unique=True,
        null=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("updated at")
    )

    user_type_choices = (
        ("normal", "normal"),
        ("petshop", "petshop"),
        ("vet", "vet"),
        ("admin", "admin"),
    )
    user_type = models.CharField(
        max_length=7, default="normal", choices=user_type_choices
    )
    register_completed = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.phone_number}-{self.get_full_name()}"

