from rest_framework.routers import DefaultRouter
from django.urls import path, include
from study_materials.views import StudyMaterialViewSet


router = DefaultRouter()
router.register("study-materials", StudyMaterialViewSet, basename="study-materials")
urlpatterns = [
    path("", include(router.urls)),
]
