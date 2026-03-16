from django.urls import path

from core.views import about, index

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
]
