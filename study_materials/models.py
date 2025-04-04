from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from subjects.models import Subject


# progress models
class Question(models.Model):
    QUESTION_TYPES = [
        ("MCQ", _("Multiple Choice")),
        ("TF", _("True/False")),
        ("ESSAY", _("Essay")),
        ("SHORT", _("Short Answer")),
    ]

    DIFFICULTY_CHOICES = [
        (1, _("Very Easy")),
        (2, _("Easy")),
        (3, _("Medium")),
        (4, _("Hard")),
        (5, _("Very Hard")),
    ]

    exam = models.ForeignKey(
        "assessments.Exam", on_delete=models.CASCADE, related_name="questions"
    )
    question_type = models.CharField(
        max_length=10, choices=QUESTION_TYPES, db_index=True
    )
    text = models.TextField()
    difficulty = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    explanation = models.TextField(blank=True)
    created_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_questions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["exam", "difficulty", "-created_at"]
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.text[:50]}..."


class StudyMaterial(models.Model):
    MATERIAL_TYPES = [
        ("PDF", "PDF"),
        ("VIDEO", "Video"),
        ("LINK", "Link"),
    ]

    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to="study_materials/files/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="materials"
    )
    chapter = models.ForeignKey(
        "subjects.Chapter",
        on_delete=models.CASCADE,
        related_name="materials",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
