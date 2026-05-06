#!/usr/bin/env python
"""Run: python seed_projects.py"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings.dev")
django.setup()

from datetime import date
from projects.models import Project

PROJECTS = [
    {
        "name": "Portfolio Site",
        "description": "Personal portfolio web app built with Django and DRF. Features a REST API, token authentication, and a vanilla JS frontend.",
        "technologies": "Django, Django REST Framework, SQLite, Vanilla JS, Docker",
        "start_date": date(2025, 1, 1),
        "end_date": date(2025, 3, 15),
    },
    {
        "name": "E-Commerce Platform",
        "description": "Full-stack online store with product catalog, shopping cart, Stripe payments, and an admin dashboard.",
        "technologies": "Django, PostgreSQL, React, Stripe API, Redis",
        "start_date": date(2024, 6, 1),
        "end_date": date(2024, 11, 30),
    },
    {
        "name": "Real-Time Chat App",
        "description": "WebSocket-based chat application supporting multiple rooms, user presence, and message history.",
        "technologies": "Django Channels, Redis, React, WebSocket",
        "start_date": date(2024, 3, 1),
        "end_date": date(2024, 5, 20),
    },
    {
        "name": "Task Management API",
        "description": "RESTful API for a kanban-style task manager with boards, columns, cards, and team collaboration.",
        "technologies": "FastAPI, PostgreSQL, SQLAlchemy, JWT, Docker Compose",
        "start_date": date(2023, 9, 1),
        "end_date": date(2023, 12, 31),
    },
    {
        "name": "Data Pipeline Dashboard",
        "description": "Internal tool for monitoring ETL pipelines. Displays run status, error logs, and throughput charts in real time.",
        "technologies": "Python, Airflow, PostgreSQL, React, Chart.js",
        "start_date": date(2023, 4, 1),
        "end_date": date(2023, 8, 15),
    },
    {
        "name": "CLI Budget Tracker",
        "description": "Command-line tool for tracking personal income and expenses with monthly reports and CSV export.",
        "technologies": "Python, Click, SQLite, Rich",
        "start_date": date(2022, 11, 1),
        "end_date": date(2023, 1, 10),
    },
    {
        "name": "ML Sentiment Analyzer",
        "description": "Microservice that classifies product reviews as positive, neutral, or negative using a fine-tuned BERT model.",
        "technologies": "Python, HuggingFace Transformers, FastAPI, Docker",
        "start_date": date(2025, 4, 1),
        "end_date": None,
    },
]

created = 0
for data in PROJECTS:
    _, new = Project.objects.get_or_create(name=data["name"], defaults=data)
    if new:
        created += 1

print(f"Done. Created {created} new project(s), {len(PROJECTS) - created} already existed.")
