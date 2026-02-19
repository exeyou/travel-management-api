from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import TravelProject, ProjectPlace
from .serializers import TravelProjectSerializer, ProjectPlaceSerializer
from django.db import transaction

class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all().order_by("-created_at")
    serializer_class = TravelProjectSerializer

    filterset_fields = ["completed", "start_date"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "start_date"]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if project.places.filter(visited=True).exists():
            return Response(
                {"error": "Cannot delete project with visited places"},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()


class ProjectPlaceViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectPlaceSerializer

    def get_queryset(self):
        return ProjectPlace.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project_id = self.kwargs["project_pk"]
        project = get_object_or_404(TravelProject, id=project_id)

        if project.places.count() >= 10:
            raise ValidationError("Maximum 10 places allowed")

        external_id = serializer.validated_data['external_id']
        artwork = get_artwork_by_id(external_id)
        title = artwork.get("title", "Unknown") if artwork else "Unknown"
        
        serializer.save(project=project, title=title)