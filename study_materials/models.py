# ersathi-backend/study_materials/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from subjects.models import Chapter, Subject
from django.conf import settings
from django.core.validators import FileExtensionValidator
from smart_selects.db_fields import ChainedForeignKey


class Question(models.Model):
    """
    Represents a Multiple Choice Question for an exam, with specific marks.
    """

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
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
    MARKS_CHOICES = [
        (1, _("1 Mark")),
        (2, _("2 Marks")),
    ]

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
    def clean(self):
        from django.core.exceptions import ValidationError

        if self.material_type == "PDF":
            if not self.file:
                raise ValidationError("PDF materials must have an uploaded PDF file.")
            if not self.file.name.lower().endswith(".pdf"):
                raise ValidationError(
                    "Only PDF files are allowed for PDF material type."
                )

        elif self.material_type == "IMAGE":
            if not self.file:
                raise ValidationError(
                    "Image materials must have an uploaded image file."
                )
            if not any(
                self.file.name.lower().endswith(ext)
                for ext in [".jpg", ".jpeg", ".png", ".gif"]
            ):
                raise ValidationError(
                    "Only image files (.jpg, .jpeg, .png, .gif) are allowed for image material type."
                )

        elif self.material_type == "VIDEO":
            if not self.file:
                raise ValidationError(
                    "Video materials must have an uploaded video file."
                )
            if not any(
                self.file.name.lower().endswith(ext)
                for ext in [".mp4", ".mov", ".avi", ".mkv"]
            ):
                raise ValidationError(
                    "Only video files (.mp4, .mov, .avi, .mkv) are allowed for video material type."
                )

        elif self.material_type == "LINK":
            if not self.url:
                raise ValidationError("Link materials must have a valid URL.")
            if self.file:
                raise ValidationError(
                    "Link materials should not have an uploaded file."
                )

        else:
            raise ValidationError("Invalid material type selected.")

    MATERIAL_TYPES = [
        ("PDF", "PDF"),
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
        ("LINK", "Link"),
    ]

    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(
        upload_to="study_materials/files/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "jpg",
                    "jpeg",
                    "png",
                    "gif",
                    "mp4",
                    "mov",
                    "avi",
                    "mkv",
                ]
            )
        ],
    )
    url = models.URLField(blank=True, null=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="materials"
    )
    chapter = models.ForeignKey(
        "subjects.Chapter",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Study Material"
        verbose_name_plural = "Study Materials"
