from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from disciplines.models import Discipline

# core models


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        related_name="students",
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(?:\+977|00977)?(?:98|97)\d{8}$",
                message="Phone number must start with '+977' or '00977' followed by a 10-digit number starting with 98 or 97.",
            ),
            MinLengthValidator(9),
        ],
        blank=True,
    )
    bio = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("student profile")
        verbose_name_plural = _("student profiles")

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.email}"
