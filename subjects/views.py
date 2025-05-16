from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Subject, Chapter
from .serializers import SubjectSerializer, ChapterSerializer
from core.permissions import IsAcademicStaffOrReadOnly


# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAcademicStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "code", "disciplines", "is_core"]
    search_fields = ["title", "description", "code"]
    ordering_fields = ["name", "code", "created_at"]
    ordering = ["code"]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"request": self.request}


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated, IsAcademicStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["subject", "chapter_number"]
    search_fields = ["title", "content", "learning_objectives"]
    ordering_fields = ["subject", "chapter_number", "created_at"]
    ordering = ["subject", "chapter_number"]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"subject_id": self.kwargs.get("subject_pk")}
