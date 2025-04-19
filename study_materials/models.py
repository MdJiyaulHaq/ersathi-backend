# ersathi-backend/study_materials/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from subjects.models import Subject
from django.conf import settings


class Question(models.Model):
    """
    Represents a Multiple Choice Question for an exam, with specific marks.
    """

    MARKS_CHOICES = [
        (1, _("1 Mark")),
        (2, _("2 Marks")),
    ]

    exam = models.ForeignKey(
        "assessments.Exam",
        on_delete=models.CASCADE,
        related_name="questions",
        help_text=_("The exam this question belongs to."),
    )
    text = models.TextField(help_text=_("The main text/body of the question."))
    marks = models.PositiveSmallIntegerField(
        choices=MARKS_CHOICES,
        default=1,
        help_text=_("Marks awarded for a correct answer."),
    )
    explanation = models.TextField(
        blank=True,
        help_text=_("Optional explanation shown after attempting the question."),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # Allow blank in admin/forms if created_by isn't mandatory there
        related_name="created_questions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True, help_text=_("Only active questions will be included in exams.")
    )

    class Meta:
        ordering = [
            "exam",
            "-marks",
            "-created_at",
        ]  # Order by exam, then marks, then creation time
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        # Updated __str__ method
        text_snippet = f"{self.text[:50]}..." if len(self.text) > 50 else self.text
        return f"MCQ ({self.marks} Mark{'s' if self.marks > 1 else ''}): {text_snippet}"

    # Note: Validation for exactly one correct answer is best handled
    # in the admin formset (see study_materials/admin.py) rather than
    # overriding the model's save() method here, as it requires checking
    # related objects which might not be saved yet during model save.


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
