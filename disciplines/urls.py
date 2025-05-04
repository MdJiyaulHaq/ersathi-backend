from rest_framework_nested import routers
from django.urls import include, path
from disciplines.views import DisciplineViewSet

router = routers.DefaultRouter()
router.register("", DisciplineViewSet, basename="disciplines")

urlpatterns = [
    path("", include(router.urls)),
]
