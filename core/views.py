from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from core.forms import (
    AddBookForm,
    AuthorForm,
    BookForm,
    CommentForm,
    MyUserCreationForm,
)
from core.models import Author, Book, Comment, Exchange

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 МБ


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "books": Book.objects.order_by("-name").all(),
    }

    return render(request, "core/index.html", context)


@login_required
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
                owner=request.user,  #  type: ignore
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
        "form": CommentForm(),
    }

    return render(request, "core/book_detail.html", context)


@login_required
def add_comment(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                book=book,
                author=request.user,  # type: ignore
                text=form.cleaned_data["text"],
            )
            messages.success(request, "Комментарий успешно добавлен")
            return redirect(reverse("core:book_detail", args=[book_id]))
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
            return redirect(reverse("core:book_detail", args=[book_id]))
    else:
        return HttpResponse("Метод не поддерживается", status=405)


def authors(request: HttpRequest) -> HttpResponse:
    context = {
        "authors": Author.objects.order_by("name").all(),
    }

    return render(request, "core/authors.html", context)


def author_detail(request: HttpRequest, author_id: int) -> HttpResponse:
    author = get_object_or_404(Author, id=author_id)

    context = {
        "author": author,
    }

    return render(request, "core/author_detail.html", context)


@login_required
def add_author(request: HttpRequest) -> HttpResponse:
    message = None
    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse("core:authors"))

        else:
            message = {
                "text": "Пожалуйста, исправьте ошибки в форме",
                "type": "error",
            }
    else:
        form = AuthorForm()

    context = {
        "form": form,
        "message": message,
    }

    return render(request, "core/add_author.html", context)


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("login"))
        else:
            error = "Пожалуйста, исправьте ошибки в форме"
            return render(
                request,
                "registration/register.html",
                {"form": form, "error": error},
            )
    else:
        form = MyUserCreationForm()
        return render(request, "registration/register.html", {"form": form})


@login_required
def edit_book(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)
    if request.user != book.owner:
        return HttpResponse(
            "У вас нет прав на редактирование этой книги", status=403
        )

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            img = form.cleaned_data["image"]
            if img and img.size > MAX_IMAGE_SIZE:
                message = {
                    "text": "Размер изображения не должен превышать 2 МБ",
                    "type": "error",
                }
                return render(
                    request,
                    "core/edit_book.html",
                    {"form": form, "book": book, "message": message},
                )

            form.save()
            return redirect(reverse("core:book_detail", args=[book_id]))
        else:
            message = {
                "text": "Пожалуйста, исправьте ошибки в форме",
                "type": "error",
            }
            return render(
                request,
                "core/edit_book.html",
                {"form": form, "book": book, "message": message},
            )
    else:
        form = BookForm(instance=book)
        return render(
            request,
            "core/edit_book.html",
            {"form": form, "book": book},
        )


@login_required
def exchange_book(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)

    if not book.is_accessible_for_exchange:
        return HttpResponse(
            "Эта книга уже взята другим пользователем", status=400
        )

    if request.user == book.owner:
        return HttpResponse(
            "Вы не можете взять в обмен свою собственную книгу", status=400
        )

    if request.method == "POST":
        Exchange.objects.create(
            book=book,
            to_user=request.user,  # type: ignore
            return_date=timezone.now()
            + timezone.timedelta(days=settings.EXCHANGE_DURATION_DAYS),  # type: ignore
        )
        return redirect(reverse("core:book_detail", args=[book_id]))

    return HttpResponse("Метод не поддерживается", status=405)
