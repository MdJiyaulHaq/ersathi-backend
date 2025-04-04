from django.db import models

# Create your models here.
# tags models


class Tag(models.Model):
    label = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(
        "study_materials.Question", related_name="tags", blank=True
    )
    study_materials = models.ManyToManyField(
        "study_materials.StudyMaterial", related_name="tags", blank=True
    )

    def __str__(self):
        return self.label
