from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(
        max_length=500,
        help_text="Comma-separated list of technologies (e.g. 'Django, Postgres').",
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "-id"]

    def __str__(self) -> str:
        return self.name
