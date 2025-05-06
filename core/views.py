from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import StudentProfile
from core.serializers import StudentProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.
def home(request):
    return render(request, "home.html")


class StudentProfileViewSet(ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["discipline"]
    search_fields = ["user__username", "user__email"]
    ordering_fields = ["user__date_joined", "user__first_name", "user__last_name"]
    ordering = ["user__date_joined"]
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["GET", "PUT", "PATCH", "OPTIONS"])
    def me(self, request):
        user_id = request.user.id
        if request.method == "GET":
            try:
                student = StudentProfile.objects.get(user_id=user_id)
                serializer = StudentProfileSerializer(student)
                return Response(serializer.data)
            except StudentProfile.DoesNotExist:
                return Response({"detail": "Profile not found."}, status=404)
            
        elif request.method in ["PUT", "PATCH"]:
            try:
                student = StudentProfile.objects.get(user_id=user_id)
                serializer = StudentProfileSerializer(
                    student, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except StudentProfile.DoesNotExist:
                return Response({"detail": "Profile not found."}, status=404)
