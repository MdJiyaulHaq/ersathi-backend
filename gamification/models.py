from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User
from django.conf import settings

# Gamification models


class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="badges/icons/", blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("badge")
        verbose_name_plural = _("badges")

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges"
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge")
        verbose_name = _("user badge")
        verbose_name_plural = _("user badges")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.badge.name}"


class Point(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="points"
    )
    value = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("point")
        verbose_name_plural = _("points")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.value} points"


class Leaderboard(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leaderboard"
    )
    total_points = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-total_points"]
        verbose_name = _("leaderboard")
        verbose_name_plural = _("leaderboards")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.total_points} points"
