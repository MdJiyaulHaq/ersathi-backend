from rest_framework_nested import routers
from django.urls import include, path
from .views import (
    BadgeViewSet,
    PointViewSet,
    UserBadgeViewSet,
    LeaderboardViewSet,
)
from rest_framework import viewsets
from rest_framework.response import Response

router = routers.DefaultRouter()
router.register(r"badges", BadgeViewSet, basename="badge")
router.register(r"points", PointViewSet, basename="point")
router.register(r"user-badges", UserBadgeViewSet, basename="user-badge")
router.register(r"leaderboard", LeaderboardViewSet, basename="leaderboard")

urlpatterns = [
    path("", include(router.urls)),
]
