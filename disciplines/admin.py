from django.contrib import admin
from .models import Discipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("related_disciplines",)
