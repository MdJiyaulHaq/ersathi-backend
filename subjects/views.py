from django.shortcuts import render
from subjects.models import Chapter, Subject
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from subjects.serializers import ChapterSerializer, SubjectSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "code", "disciplines", "is_core"]
    search_fields = ["title", "description", "code"]
    ordering_fields = ["name", "code", "created_at"]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"request": self.request}


class ChapterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        subject_id = self.kwargs.get("subject_pk")
        return Chapter.objects.filter(subject_id=subject_id)

    serializer_class = ChapterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "subject",
        "chapter_number",
        "title",
        "estimated_duration_hours",
    ]
    search_fields = ["title", "content", "learning_objectives"]
    ordering_fields = [
        "chapter_number",
        "title",
        "estimated_duration_hours",
    ]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"subject_id": self.kwargs.get("subject_pk")}
