from django.shortcuts import render
from .serializers import StudyMaterialSerializer
from django.shortcuts import render
from study_materials.models import StudyMaterial
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class StudyMaterialViewSet(viewsets.ModelViewSet):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "material_type", "subject", "chapter"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"request": self.request}
