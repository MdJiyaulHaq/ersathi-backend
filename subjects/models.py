from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# subjects models


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    disciplines = models.ManyToManyField(
        "disciplines.Discipline", related_name="subjects"
    )
    is_core = models.BooleanField(default=True)
    description = models.TextField()
    prerequisites = models.ManyToManyField(
        "self", symmetrical=False, related_name="required_for", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code", "name"]
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Chapter(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="chapters"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    chapter_number = models.PositiveIntegerField(unique=True)
    content = RichTextUploadingField()
    video_url = models.URLField(blank=True)
    learning_objectives = RichTextField(blank=True)
    estimated_duration_hours = models.PositiveIntegerField(
        help_text=_("Estimated time to complete in hours")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["subject", "chapter_number"]
        unique_together = ["subject", "chapter_number"]
        verbose_name = _("chapter")
        verbose_name_plural = _("chapters")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.code} - Chapter {self.chapter_number}: {self.title}"
