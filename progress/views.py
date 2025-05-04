from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from progress.models import ChapterProgress, QuestionAttempt
from .serializers import ChapterProgressSerializer, QuestionAttemptSerializer


# Create your views here.
class QuestionAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return QuestionAttempt.objects.filter(student=user)

    serializer_class = QuestionAttemptSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["student", "question", "selected_answer", "is_correct"]
    search_fields = ["student__username", "question__text"]
    ordering_fields = ["answered_at"]
    ordering = ["-answered_at"]
    pagination_class = PageNumberPagination


class ChapterProgressViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return ChapterProgress.objects.filter(student=user)

    serializer_class = ChapterProgressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "student",
        "chapter",
        "completion_percentage",
    ]
    search_fields = ["student__username", "chapter__title"]
    ordering_fields = ["completion_percentage", "start_date", "completion_date"]
    ordering = ["-last_accessed"]
    pagination_class = PageNumberPagination
