from django.urls import path

from core.views import (
    AddBookView,
    BookDetailView,
    BookListView,
    EditBookView,
    about,
    add_author,
    add_comment,
    author_detail,
    authors,
    exchange_book,
    register,
)

app_name = "core"

urlpatterns = [
    path("", BookListView.as_view(), name="index"),
    path("register/", register, name="register"),
    path("about/", about, name="about"),
    path("book/<int:book_id>/", BookDetailView.as_view(), name="book_detail"),
    path("add_book/", AddBookView.as_view(), name="add_book"),
    path("add_author/", add_author, name="add_author"),
    path("authors/", authors, name="authors"),
    path("author/<int:author_id>/", author_detail, name="author_detail"),
    path("book/<int:book_id>/edit/", EditBookView.as_view(), name="edit_book"),
    path("book/<int:book_id>/exchange/", exchange_book, name="exchange_book"),
    path("book/<int:book_id>/add-comment/", add_comment, name="add_comment"),
]
