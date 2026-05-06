from django.urls import path

from frontend.views import CreateProjectView, IndexView, LoginView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("projects/new/", CreateProjectView.as_view(), name="project-create"),
]
