from rest_framework import serializers
from questions.models import Question
from .models import AnswerOption
from subjects.models import Chapter, Subject


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "subject",
            "chapter",
            "marks",
            "text",
            "explanation",
            "created_by",
            "is_active",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "subject": {"required": True},
            "chapter": {"required": True},
            "marks": {"required": True},
            "text": {"required": True},
            "explanation": {"required": False},
            "is_active": {"required": False},
        }


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = [
            "id",
            "question",
            "text",
            "is_correct",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "question": {"required": True},
            "text": {"required": True},
            "is_correct": {"required": True},
        }


class NestedAnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["text", "is_correct"]


class QuestionCreateSerializer(serializers.ModelSerializer):
    answer_options = NestedAnswerOptionSerializer(many=True, write_only=True)
    answer_options_response = AnswerOptionSerializer(source="answeroption_set", many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "subject",
            "chapter",
            "marks",
            "text",
            "explanation",
            "created_by",
            "is_active",
            "answer_options",
            "answer_options_response",
        ]

    def validate(self, data):
        options = data.get("answer_options", [])
        if len(options) != 4:
            raise serializers.ValidationError("Exactly 4 answer options are required.")
        correct_count = sum(1 for opt in options if opt.get("is_correct"))
        if correct_count != 1:
            raise serializers.ValidationError(
                "Exactly one option must be marked as correct."
            )
        return data

    def create(self, validated_data):
        options_data = validated_data.pop("answer_options")
        request = self.context.get("request")
        question = Question.objects.create(created_by=request.user, **validated_data)
        for option_data in options_data:
            AnswerOption.objects.create(question=question, **option_data)
        return question
