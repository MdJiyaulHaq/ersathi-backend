from gamification.models import UserBadge, Badge, Point, Leaderboard
from rest_framework import viewsets, permissions
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    UserBadgeSerializer,
    BadgeSerializer,
    PointSerializer,
    LeaderboardSerializer,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated


# Create your views here.
class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "description", "active"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserBadgeViewSet(viewsets.ModelViewSet):
    serializer_class = UserBadgeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["user", "badge", "awarded_at", "active"]
    search_fields = ["user__username", "badge__name"]
    ordering_fields = ["awarded_at"]
    ordering = ["-awarded_at"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserBadge.objects.all()
        return UserBadge.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PointViewSet(viewsets.ModelViewSet):
    serializer_class = PointSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["user", "value", "reason", "type", "created_at"]
    search_fields = ["user__username", "reason"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return Point.objects.all()
        return Point.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["user", "total_points", "last_updated"]
    search_fields = ["user__username"]
    ordering_fields = ["total_points", "last_updated"]
    ordering = ["-total_points"]
    pagination_class = PageNumberPagination
