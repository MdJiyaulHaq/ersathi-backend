from django.shortcuts import render
from .serializers import StudyMaterialSerializer
from study_materials.models import StudyMaterial
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from core.permissions import IsAcademicStaffOrReadOnly


class StudyMaterialViewSet(viewsets.ModelViewSet):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsAcademicStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "material_type", "subject", "chapter"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
