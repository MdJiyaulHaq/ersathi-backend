from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from subjects.models import Subject, Chapter
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MinValueValidator


class Question(models.Model):

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
        blank=True,
        related_name="created_questions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True, help_text=_("Only active questions will be included in exams.")
    )

    class Meta:
        ordering = ["-marks", "-created_at"]
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        text_snippet = f"{self.text[:50]}..." if len(self.text) > 50 else self.text
        return f"MCQ ({self.marks} Mark{'s' if self.marks > 1 else ''}): {text_snippet}"


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"
