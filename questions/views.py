from django.shortcuts import render
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import AnswerOption, Question
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import QuestionSerializer, AnswerOptionSerializer, QuestionCreateSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "subject",
        "chapter",
        "marks",
        "text",
        "explanation",
        "created_by",
        "is_active",
    ]
    ordering_fields = ["created_at", "marks"]
    search_fields = ["text", "explanation", "created_by"]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "create":
            return QuestionCreateSerializer
        return QuestionSerializer


class AnswerOptionViewSet(viewsets.ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "question",
        "text",
        "is_correct",
        "created_by",
    ]
    ordering_fields = ["updated_at", "created_at"]
    search_fields = ["text", "created_by"]
    pagination_class = PageNumberPagination
