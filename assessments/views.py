from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Exam, ExamAttempt
from .serializers import ExamSerializer, ExamAttemptSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta


# Create your views here.
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "exam_type", "subject__name"]
    ordering_fields = ["start_date", "created_at"]
    ordering = ["start_date", "passing_score", "duration", "created_at"]
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="start", url_name="start-exam")
    def start_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        # Check if the user has already attempted this exam
        if ExamAttempt.objects.filter(exam=exam, student=user).exists():
            return Response({"detail": "You have already attempted this exam."}, status=status.HTTP_400_BAD_REQUEST)

        start_time = timezone.now()
        end_time = start_time + timedelta(minutes=exam.duration)

        attempt = ExamAttempt.objects.create(
            exam=exam,
            student=user,
            start_time=start_time,
            end_time=end_time,
        )

        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExamAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = ExamAttempt.objects.filter(student=self.request.user).select_related("exam")
        exam_id = self.kwargs.get("exam_pk")
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        return queryset

    serializer_class = ExamAttemptSerializer
    # permission_classes = [permissions.IsAuthenticated]
