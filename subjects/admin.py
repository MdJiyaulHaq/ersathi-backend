from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Subject, Chapter


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_core", "created_at")
    list_filter = ("is_core", "disciplines")
    search_fields = ("name", "code", "description")
    filter_horizontal = ("prerequisites", "disciplines")
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "chapter_number", "estimated_duration")
    list_filter = ("subject", "created_at")
    search_fields = ("title", "content", "learning_objectives")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["subject"]
    list_per_page = 20

    fieldsets = (
        (None, {"fields": ("subject", "title", "slug", "chapter_number")}),
        (_("Content"), {"fields": ("content", "video_url", "learning_objectives")}),
        (_("Duration"), {"fields": ("estimated_duration",), "classes": ("collapse",)}),
    )
