from django.urls import path

from core.views import (
    about,
    add_author,
    add_book,
    author_detail,
    authors,
    book_detail,
    edit_book,
    exchange_book,
    index,
    register,
)

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("about/", about, name="about"),
    path("book/<int:book_id>/", book_detail, name="book_detail"),
    path("add_book/", add_book, name="add_book"),
    path("add_author/", add_author, name="add_author"),
    path("authors/", authors, name="authors"),
    path("author/<int:author_id>/", author_detail, name="author_detail"),
    path("book/<int:book_id>/edit/", edit_book, name="edit_book"),
    path("book/<int:book_id>/exchange/", exchange_book, name="exchange_book"),
]
