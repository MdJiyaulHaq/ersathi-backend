from django.db import models


# disciplines models
# Create your models here.
class Discipline(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Civil Engineering"
    slug = models.SlugField(unique=True)
    description = models.TextField()
    related_disciplines = models.ManyToManyField("self", blank=True)
