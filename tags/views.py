from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from tags.models import Tag
from tags.serializers import TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from core.permissions import IsAdminOrReadOnly


# Create your views here.
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["label", "slug"]
    search_fields = ["label", "slug"]
    ordering_fields = ["created_at", "slug"]
    pagination_class = PageNumberPagination
