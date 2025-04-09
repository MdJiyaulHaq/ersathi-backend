from django.contrib import admin
from .models import Subject, Chapter


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_core")
    search_fields = ("name", "code", "description")
    list_filter = ("is_core", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "chapter_number")
    search_fields = ("title", "content", "subject__name")
    list_filter = ("subject", "created_at")
    prepopulated_fields = {"slug": ("title",)}
