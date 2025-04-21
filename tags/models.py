from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
# tags models


class Tag(models.Model):
    label = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label


# Define a TaggedItem model to associate tags with any model instance
class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # If a tag is deleted, it should be removed from all the associated objects.

    # Type (product, video, article, etc)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Object_ID to identify any objects or any records in any tables
    object_id = models.PositiveIntegerField()

    # GenericForeignKey to create a generic relation to any model instance
    content_object = GenericForeignKey()
