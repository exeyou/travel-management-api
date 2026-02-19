from django.db import models
from django.core.exceptions import ValidationError


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def update_completion_status(self):
        total_places = self.places.count()
        if total_places > 0 and all(place.visited for place in self.places.all()):
            self.completed = True
        else:
            self.completed = False
        self.save()

    def delete(self, *args, **kwargs):
        if self.places.filter(visited=True).exists():
            raise ValidationError("Cannot delete project with visited places")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject,
        related_name='places',
        on_delete=models.CASCADE
    )

    external_id = models.IntegerField()
    title = models.CharField(max_length=255, blank=True)

    notes = models.TextField(blank=True, null=True)
    visited = models.BooleanField(default=False)
    visited_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'external_id')

    def clean(self):
        if self.project.places.count() >= 10 and not self.pk:
            raise ValidationError("Maximum 10 places allowed per project")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.project.update_completion_status()

    def __str__(self):
        return f"{self.title} ({self.external_id})"
