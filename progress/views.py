from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from progress.models import ChapterProgress, QuestionAttempt
from .serializers import ChapterProgressSerializer, QuestionAttemptSerializer
from core.permissions import IsOwnerOrStaff


# Create your views here.
class QuestionAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionAttemptSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["question", "is_correct", "answered_at"]
    search_fields = ["student__username", "question__text"]
    ordering_fields = ["answered_at", "time_taken"]
    ordering = ["-answered_at"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return QuestionAttempt.objects.all()
        return QuestionAttempt.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ChapterProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterProgressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["chapter", "completion_percentage", "completion_date"]
    search_fields = ["chapter__title", "student__username"]
    ordering_fields = ["start_date", "completion_date", "last_accessed"]
    ordering = ["-last_accessed"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return ChapterProgress.objects.all()
        return ChapterProgress.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
