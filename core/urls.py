from django.urls import include, path
from core import views
from rest_framework_nested import routers
from .views import StudentProfileViewSet

app_name = "core"
router = routers.DefaultRouter()
router.register(
    "student-profiles", views.StudentProfileViewSet, basename="student-profile"
)

urlpatterns = [
    path("", views.home, name="home"),
    path("core/", include(router.urls)),
]
