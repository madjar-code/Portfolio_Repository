from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from projects.models import Project

User = get_user_model()


class ProjectAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="alice", password="pw12345!")
        self.token = Token.objects.create(user=self.user)
        Project.objects.create(
            name="Alpha",
            description="d",
            technologies="t",
            start_date=date(2024, 1, 1),
        )

    def test_anonymous_can_list_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_project(self):
        response = self.client.post(
            "/api/projects/",
            {
                "name": "New",
                "description": "x",
                "technologies": "t",
                "start_date": "2024-01-01",
            },
            format="json",
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_authenticated_can_create_project(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            "/api/projects/",
            {
                "name": "New",
                "description": "x",
                "technologies": "t",
                "start_date": "2024-01-01",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
