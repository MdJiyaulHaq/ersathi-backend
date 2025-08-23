from django.conf import settings
from .models import StudentProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class StudentProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_id",
            "university",
            "program",
            "phone",
            "bio",
            "date_of_birth",
        ]
        read_only_fields = ["user_id"]
