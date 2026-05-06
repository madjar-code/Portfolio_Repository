from django.urls import path
from rest_framework.routers import DefaultRouter

from projects.api.views import ObtainAuthTokenView, ProjectViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("auth/token/", ObtainAuthTokenView.as_view(), name="api-token"),
    *router.urls,
]
