from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.models import Book


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "books": Book.objects.order_by("-name").all(),
    }

    return render(request, "core/index.html", context)


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
