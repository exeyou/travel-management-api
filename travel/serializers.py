from rest_framework import serializers
from .models import TravelProject, ProjectPlace
from .services import get_artwork_by_id
from django.utils import timezone
from django.db import transaction

class ProjectPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectPlace
        fields = [
            "id",
            "external_id",
            "title",
            "notes",
            "visited",
            "visited_at",
            "created_at"
        ]
        read_only_fields = ["title", "visited_at", "created_at"]

    def validate_external_id(self, value):
        artwork = get_artwork_by_id(value)

        if not artwork:
            raise serializers.ValidationError(
                "Artwork does not exist in Art Institute API."
            )

        return value

    def create(self, validated_data):
        external_id = validated_data["external_id"]
        artwork = get_artwork_by_id(external_id)

        validated_data["title"] = artwork.get("title")

        return super().create(validated_data)

    def update(self, instance, validated_data):

        if "visited" in validated_data and validated_data["visited"] and not instance.visited:
            instance.visited_at = timezone.now()

        return super().update(instance, validated_data)


class TravelProjectSerializer(serializers.ModelSerializer):

    places = ProjectPlaceSerializer(many=True, required=True)

    class Meta:
        model = TravelProject
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "completed",
            "places",
            "created_at"
        ]
        read_only_fields = ["completed", "created_at"]

    def validate_places(self, value):
        if not value or len(value) < 1:
            raise serializers.ValidationError("Project must have at least one place")

        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 places allowed.")

        external_ids = [place["external_id"] for place in value]

        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError("Duplicate external_id detected.")

        return value

    def create(self, validated_data):
        places_data = validated_data.pop("places", [])
        
        with transaction.atomic():
            project = TravelProject.objects.create(**validated_data)

            for place_data in places_data:
                artwork = get_artwork_by_id(place_data["external_id"])
                place_title = artwork.get("title") if artwork else "Unknown Artwork"
                
                ProjectPlace.objects.create(
                    project=project, 
                    title=place_title, 
                    **place_data
                )

        return project
