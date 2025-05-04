from rest_framework import serializers
from progress.models import QuestionAttempt, ChapterProgress


class ChapterProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterProgress
        fields = [
            "id",
            "student",
            "chapter",
            "completion_percentage",
            "start_date",
            "completion_date",
            "last_accessed",
        ]


class QuestionAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = [
            "id",
            "student",
            "question",
            "selected_answer",
            "is_correct",
            "answered_at",
        ]
