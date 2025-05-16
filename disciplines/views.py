from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Discipline
from .serializers import DisciplineSerializer
from core.permissions import IsAcademicStaffOrReadOnly


# Create your views here.
class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [permissions.IsAuthenticated, IsAcademicStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]
    ordering = ["name"]
    pagination_class = PageNumberPagination
