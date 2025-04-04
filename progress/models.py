from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

# progress models


class ChapterProgress(models.Model):
    student = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="chapter_progress"
    )
    chapter = models.ForeignKey(
        "subjects.Chapter", on_delete=models.CASCADE, related_name="student_progress"
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

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.chapter}"


class QuestionAttempt(models.Model):
    student = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="question_attempts"
    )
    exam = models.ForeignKey(
        "assessments.Exam", on_delete=models.CASCADE, related_name="question_attempts"
    )
    question = models.ForeignKey(
        "study_materials.Question", on_delete=models.CASCADE, related_name="attempts"
    )
    selected_answer = models.ForeignKey(
        "assessments.AnswerOption",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attempts",
    )
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    time_taken = models.PositiveIntegerField(
        help_text=_("Time taken in seconds"), null=True
    )

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = _("question attempt")
        verbose_name_plural = _("question attempts")

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.question}"
