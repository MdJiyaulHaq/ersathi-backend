from django.contrib import admin
from .models import Question, StudyMaterial


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "question_type", "difficulty", "exam", "is_active")
    search_fields = ("text", "explanation")
    list_filter = ("question_type", "difficulty", "is_active", "created_at")


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "material_type", "subject", "chapter")
    search_fields = ("title", "subject__name", "chapter__title")
    list_filter = ("material_type", "created_at")
