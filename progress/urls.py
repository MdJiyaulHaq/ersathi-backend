from rest_framework_nested import routers
from django.urls import path, include

from progress.views import QuestionAttemptViewSet


routers = routers.DefaultRouter()
routers.register(
    "question-attempts", QuestionAttemptViewSet, basename="question-attempts"
)
routers.register(
    "chapter-progress", QuestionAttemptViewSet, basename="chapter-progress"
)
urlpatterns = [
    path("", include(routers.urls)),
]
