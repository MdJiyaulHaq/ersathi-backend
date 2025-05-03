# ersathi-backend/study_materials/admin.py

from django.contrib import admin
from .models import StudyMaterial


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ["title", "material_type", "subject", "chapter", "created_at"]
    list_filter = ["material_type", "subject", "is_active", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]
