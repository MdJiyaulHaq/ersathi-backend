from rest_framework import serializers
from likes.models import LikedItem


class LikedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedItem
        fields = ["id", "student", "content_type", "object_id", "created_at"]
        read_only_fields = ["student", "created_at"]
