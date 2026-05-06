from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken

from projects.api.filters import ProjectFilter
from projects.api.permissions import ReadOnlyOrAuthenticated
from projects.api.serializers import ProjectSerializer
from projects.models import Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (ReadOnlyOrAuthenticated,)
    filterset_class = ProjectFilter
    search_fields = ("name", "description", "technologies")
    ordering_fields = ("name", "start_date", "end_date", "created_at")
    ordering = ("-start_date",)


class ObtainAuthTokenView(ObtainAuthToken):
    """Token-issuing endpoint without SessionAuthentication.

    The default ObtainAuthToken inherits the project-wide auth classes, which
    include SessionAuthentication. SessionAuthentication enforces CSRF on
    unsafe requests; that breaks AJAX logins from the JS frontend, which has a
    Django session cookie (from /admin/) but no CSRF token. Empty
    authentication_classes makes this endpoint pure username/password.
    """

    authentication_classes = ()
