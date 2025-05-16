from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import LikedItem
from .serializers import LikedItemSerializer
from core.permissions import IsOwnerOrStaff


class LikedItemViewSet(viewsets.ModelViewSet):
    serializer_class = LikedItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["content_type", "object_id"]
    search_fields = ["student__user__username"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return LikedItem.objects.all()
        return LikedItem.objects.filter(student=self.request.user.student_profile)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(student=self.request.user.student_profile)
        else:
            raise PermissionDenied("You must be logged in to like an item.")

    def destroy(self, request, *args, **kwargs):
        liked_item = self.get_object()
        if liked_item.student != request.user.student_profile:
            return Response(
                {"message": "You can only unlike your own items."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        liked_item.delete()
        return Response(
            {"message": "Item unliked successfully!"}, status=status.HTTP_204_NO_CONTENT
        )
