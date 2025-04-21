from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Define a Item model to associate Like with any model instance
class LikedItem(models.Model):
    student = models.ForeignKey(
        "core.StudentProfile", on_delete=models.CASCADE, related_name="liked_items"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["student", "content_type", "object_id"]

    def __str__(self):
        return f"{self.student.user.get_full_name()} liked {self.content_object}"
