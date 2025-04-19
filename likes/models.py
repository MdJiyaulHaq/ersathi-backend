from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
# likes models


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(
        "study_materials.Question", related_name="likes", blank=True
    )
    study_materials = models.ManyToManyField(
        "study_materials.StudyMaterial", related_name="likes", blank=True
    )


# Define a Item model to associate Like with any model instance
class LikedItem(models.Model):
    # what Like applied to what object
    like = models.ForeignKey(Like, on_delete=models.CASCADE)

    # Type (product, video, article, etc)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Object_ID to identify any objects or any records in any tables
    object_id = models.PositiveIntegerField()

    # GenericForeignKey to create a generic relation to any model instance
    content_object = GenericForeignKey()
