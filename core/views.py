from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import StudentProfile
from core.serializers import StudentProfileSerializer


# Create your views here.
def home(request):
    return render(request, "home.html")


class StudentProfileView(ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["discipline"]
    search_fields = ["user__username", "user__email"]
    ordering_fields = ["user__date_joined", "user__first_name", "user__last_name"]
    ordering = ["user__date_joined"]
    pagination_class = PageNumberPagination
