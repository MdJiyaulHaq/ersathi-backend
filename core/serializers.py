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
            "user_id",
            "discipline",
            "phone",
            "bio",
            "date_of_birth",
        ]
        read_only_fields = ["user_id"]
