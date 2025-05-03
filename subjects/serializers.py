from rest_framework import serializers
from subjects.models import Subject, Chapter


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "pk",
            "name",
            "code",
            "disciplines",
            "is_core",
            "description",
            "prerequisites",
        ]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            "pk",
            "subject",
            "title",
            "chapter_number",
            "content",
            "video_url",
            "learning_objectives",
            "estimated_duration_hours",
        ]
        read_only_fields = ["subject"]

    def create(self, validated_data):
        subject_id = self.context.get("subject_id")
        return Chapter.objects.create(subject_id=subject_id, **validated_data)
