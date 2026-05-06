from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from projects.models import Project

User = get_user_model()


class ProjectCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username="bob", password="pw12345!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_persists_and_delete_removes(self):
        create_response = self.client.post(
            "/api/projects/",
            {
                "name": "Created",
                "description": "x",
                "technologies": "t",
                "start_date": "2024-01-01",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        project_id = create_response.data["id"]
        self.assertTrue(Project.objects.filter(id=project_id).exists())

        delete_response = self.client.delete(f"/api/projects/{project_id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=project_id).exists())

    def test_create_rejects_end_before_start(self):
        response = self.client.post(
            "/api/projects/",
            {
                "name": "Bad dates",
                "description": "x",
                "technologies": "t",
                "start_date": "2024-06-01",
                "end_date": "2024-01-01",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("end_date", response.data)
