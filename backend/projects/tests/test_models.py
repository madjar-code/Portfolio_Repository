from datetime import date

from django.test import TestCase

from projects.models import Project


class ProjectModelTests(TestCase):
    def test_create_and_str(self):
        project = Project.objects.create(
            name="Portfolio site",
            description="Personal portfolio",
            technologies="Django, DRF",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 6, 1),
        )

        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(str(project), "Portfolio site")
