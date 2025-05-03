# ersathi-backend/study_materials/models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from subjects.models import Subject, Chapter
from django.core.validators import FileExtensionValidator
from smart_selects.db_fields import ChainedForeignKey


class StudyMaterial(models.Model):
    class MaterialType(models.TextChoices):
        NOTE = "NOTE", "Note"
        SYLLABUS = "SYLLABUS", "Syllabus"
        PAST_PAPER = "PAST_PAPER", "Past Paper"
        PRACTICE_SET = "PRACTICE_SET", "Practice Set"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(
        max_length=20,
        choices=MaterialType.choices,
        default=MaterialType.NOTE,
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="materials"
    )
    chapter = ChainedForeignKey(
        Chapter,
        chained_field="subject",
        chained_model_field="subject",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to="study_materials/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf", "doc", "docx", "odf", "odt", "txt",
                    "jpg", "jpeg", "png", "svg",
                    "ppt", "pptx", "xls", "xlsx", "csv",
                    "mp4", "mov", "webm", "mp3", "wav",
                ]
            )
        ],
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_materials",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"
