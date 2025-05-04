from rest_framework_nested import routers
from django.urls import path, include
from .views import QuestionViewSet, AnswerOptionViewSet
from django.conf import settings


router = routers.DefaultRouter()
router.register("", QuestionViewSet, basename="questions")


urlpatterns = [
    path("", include(router.urls)),
]
