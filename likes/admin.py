from django.contrib import admin
from .models import Like, LikedItem


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    date_hierarchy = "created_at"
    filter_horizontal = ("questions", "study_materials")
    search_fields = ("id", "questions__title", "study_materials__title")


@admin.register(LikedItem)
class LikedItemAdmin(admin.ModelAdmin):
    list_display = ("like", "content_type", "object_id")
    list_filter = ("content_type",)
    autocomplete_fields = ["like"]
    search_fields = ("object_id", "like__title")
