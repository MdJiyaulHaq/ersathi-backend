from datetime import timedelta
from django.db import models
from subjects.models import Subject
from core.models import User
from study_materials.models import Question
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# assessments models
class Exam(models.Model):
    class ExamType(models.TextChoices):
        MOCK_TEST = "MOCK", "Mock Test"
        SUBJECT_TEST = "SUBJECT", "Subject Test"
        CHAPTER_QUIZ = "CHAPTER", "Chapter Quiz"
        PAST_PAPER = "PAST", "Past Paper"

    exam_type = models.CharField(
        max_length=10,
        choices=ExamType.choices,
        default=ExamType.MOCK_TEST,
        db_index=True,
        help_text="Select the category of the exam.",
    )
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exams")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    passing_score = models.PositiveIntegerField(
        default=50, validators=[MinValueValidator(50), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.duration:
            self.end_date = self.start_date + timedelta(minutes=self.duration)
        else:
            self.end_date = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_exam_type_display()}: {self.title} ({self.subject})"


class ExamAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_attempts"
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="attempts")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.exam} ({self.score})"


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"
