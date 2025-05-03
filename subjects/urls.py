from django.urls import include, path
from .views import SubjectViewSet, ChapterViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("", SubjectViewSet, basename="subjects")
subject_router = routers.NestedDefaultRouter(router, "", lookup="subject")
subject_router.register("chapters", ChapterViewSet, basename="subject-chapters")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(subject_router.urls)),
]
