from rest_framework import serializers

from study_materials.models import StudyMaterial


class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = [
            "id",
            "title",
            "description",
            "material_type",
            "subject",
            "chapter",
            "file",
            "is_active",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "title": {"required": True},
            "material_type": {"required": True},
            "subject": {"required": True},
            "chapter": {"required": True},
            "file": {"required": True},
            "is_active": {"required": False},
        }
