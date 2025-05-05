from rest_framework_nested import routers

# from tags.views import TagViewSet
from tags.views import TagViewSet
from django.urls import path, include

routers = routers.DefaultRouter()
routers.register("", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(routers.urls)),
]
