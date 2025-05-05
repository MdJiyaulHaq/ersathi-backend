from rest_framework_nested import routers
from likes.views import LikedItemViewSet
from django.urls import path, include
from django.conf import settings

routers = routers.DefaultRouter()
routers.register("liked-items", LikedItemViewSet, basename="liked-items")

urlpatterns = [
    path("", include(routers.urls)),
]
