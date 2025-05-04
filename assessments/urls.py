from rest_framework_nested import routers
from django.urls import path, include
from . import views

# Root router
router = routers.DefaultRouter()
router.register("exams", views.ExamViewSet, basename="exam")

# Nested router for ExamAttempts under exams
exam_router = routers.NestedDefaultRouter(router, r"exams", lookup="exam")
exam_router.register("attempts", views.ExamAttemptViewSet, basename="exam-attempts")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(exam_router.urls)),
]
