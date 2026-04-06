from django.urls import path

from core.views import about, book_detail, index

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("book/<int:book_id>/", book_detail, name="book_detail"),
]
