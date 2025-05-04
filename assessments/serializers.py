from datetime import timedelta, timezone
from rest_framework import serializers
from .models import Exam, ExamAttempt
from questions.serializers import QuestionSerializer, AnswerOptionSerializer


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["id", "title", "description", "subject", "exam_type", "created_by", "duration", "passing_score"]
        read_only_fields = ["created_at", "created_by", "start_date", "end_date"]
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": False},
            "subject": {"required": True},
            "duration": {"required": True},
            "passing_score": {"required": True},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Exam.objects.all(),
                fields=["title", "subject"],
                message="An exam with this title and subject already exists.",
            )
        ]

    def validate(self, attrs):
        if attrs.get("start_date") and attrs.get("duration"):
            end_date = attrs["start_date"] + timedelta(minutes=attrs["duration"])
            if end_date < timezone.now():
                raise serializers.ValidationError("The end date must be in the future.")
        if attrs.get("exam_type") and attrs["exam_type"] not in Exam.ExamType.values:
            raise serializers.ValidationError("Invalid exam type.")
        return super().validate(attrs)

    def create(self, validated_data):
        exam = super().create(validated_data)
        return exam

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.subject = validated_data.get("subject", instance.subject)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.passing_score = validated_data.get(
            "passing_score", instance.passing_score
        )
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.save()
        return instance


class ExamAttemptSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ExamAttempt
        fields = ["id", "student", "exam", "start_time", "end_time", "score", "status"]
        read_only_fields = ["start_time", "end_time"]
