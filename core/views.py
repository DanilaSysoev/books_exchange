from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.forms import AddBookForm
from core.models import Author, Book

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 МБ


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "books": Book.objects.order_by("-name").all(),
    }

    return render(request, "core/index.html", context)


def add_book(request: HttpRequest) -> HttpResponse:
    message = None
    if request.method == "POST":
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            author = Author.objects.create(name=form.cleaned_data["author"])
            img = form.cleaned_data["image"]
            if img and img.size > MAX_IMAGE_SIZE:
                message = {
                    "text": "Размер изображения не должен превышать 2 МБ",
                    "type": "error",
                }
                return render(
                    request,
                    "core/add_book.html",
                    {"message": message, "form": form},
                )

            Book.objects.create(
                name=form.cleaned_data["name"],
                publish_year=form.cleaned_data["publish_year"],
                annotation=form.cleaned_data["annotation"],
                author=author,
                image=img,
            )

            message = {
                "text": "Книга успешно добавлена",
                "type": "success",
            }

            return render(
                request,
                "core/add_book.html",
                {"message": message, "form": AddBookForm()},
            )
        else:
            message = {
                "text": "Пожалуйста, исправьте ошибки в форме",
                "type": "error",
            }
    else:
        form = AddBookForm()

    context = {
        "form": form,
        "message": message,
    }

    return render(request, "core/add_book.html", context)


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "my_url": reverse("core:about"),
    }

    return render(request, "core/about.html", context)


def book_detail(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)

    context = {
        "book": book,
    }

    return render(request, "core/book_detail.html", context)
