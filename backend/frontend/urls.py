from django.urls import path

from frontend.views import IndexView, LoginView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
]
