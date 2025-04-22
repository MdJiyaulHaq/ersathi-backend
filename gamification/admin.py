from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Badge, UserBadge, Point, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "created_at")
    list_filter = ("active", "created_at")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "active", "awarded_at")
    list_filter = ("active", "badge", "awarded_at")
    search_fields = ("user__username", "user__email", "badge__name")
    date_hierarchy = "awarded_at"
    autocomplete_fields = ["user", "badge"]
    readonly_fields = ("awarded_at",)


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("user", "value", "type", "reason", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("user__username", "user__email", "reason")
    date_hierarchy = "created_at"
    autocomplete_fields = ["user"]

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("user", "total_points", "last_updated")
    search_fields = ("user__username", "user__email")
    ordering = ("-total_points",)
    autocomplete_fields = ["user"]
    list_filter = ("total_points",)
