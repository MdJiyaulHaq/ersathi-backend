from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from subjects.models import Chapter
from questions.models import Question, AnswerOption

# progress models


class ChapterProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chapter_progress",
    )
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="student_progress"
    )
    completion_percentage = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "chapter"]
        verbose_name = _("chapter progress")
        verbose_name_plural = _("chapter progress")

    @property
    def is_completed(self):
        return self.completion_percentage == 100

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.chapter}"

    def save(self, *args, **kwargs):
        if self.completion_percentage == 100 and not self.completion_date:
            self.completion_date = timezone.now()
        super().save(*args, **kwargs)


class QuestionAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="question_attempts",
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="attempts"
    )
    selected_answer = models.ForeignKey(
        AnswerOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attempts",
    )
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.PositiveIntegerField(
        help_text=_("Time taken in seconds"),
        null=True,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("question attempt")
        verbose_name_plural = _("question attempts")
        unique_together = ["student", "question"]

    def __str__(self):
        correctness = "✔️" if self.is_correct else "❌"
        return f"{self.student.get_full_name()} - {self.question} [{correctness}]"
