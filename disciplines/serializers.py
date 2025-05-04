from disciplines.models import Discipline
from rest_framework import serializers


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["id", "name", "slug", "description"]

        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Discipline name cannot be blank.",
                    "required": "Discipline name is required.",
                }
            },
            "slug": {
                "error_messages": {
                    "blank": "Slug cannot be blank.",
                    "required": "Slug is required.",
                }
            },
        }
