from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from projects.models import Project


class ProjectAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.alpha = Project.objects.create(
            name="Django blog",
            description="Personal blog",
            technologies="Django, Postgres",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 6, 1),
        )
        self.beta = Project.objects.create(
            name="React dashboard",
            description="Admin dashboard built with React",
            technologies="React, TypeScript",
            start_date=date(2024, 5, 1),
        )

    def test_list_returns_paginated_results(self):
        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertIn("results", response.data)

    def test_retrieve_unknown_id_returns_404(self):
        response = self.client.get("/api/projects/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_matches_description(self):
        response = self.client.get("/api/projects/?search=dashboard")

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "React dashboard")

    def test_ordering_by_start_date_desc(self):
        response = self.client.get("/api/projects/?ordering=-start_date")

        names = [p["name"] for p in response.data["results"]]
        self.assertEqual(names, ["React dashboard", "Django blog"])
