from django.contrib import admin
from .models import LikedItem


@admin.register(LikedItem)
class LikedItemAdmin(admin.ModelAdmin):
    list_display = ("student", "content_type", "object_id", "created_at")
    list_filter = ("created_at", "student", "content_type")
    search_fields = ("student__user__username", "student__user__email", "object_id")
    readonly_fields = (
        "student",
        "content_type",
        "object_id",
        "content_object",
        "created_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at", "student", "content_type")

    def has_add_permission(self, request):
        return False
