from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "books": [
            {"title": "Книга 1", "author": "Автор 1"},
            {"title": "Книга 2", "author": "Автор 2"},
            {"title": "Книга 3", "author": "Автор 3"},
        ],
        "error": None,
    }

    return render(request, "core/index.html", context)


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "my_url": reverse("core:about"),
    }

    return render(request, "core/about.html", context)
