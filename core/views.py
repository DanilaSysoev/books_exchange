from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.forms import (
    AuthorForm,
    BookForm,
    CommentForm,
    MyUserCreationForm,
)
from core.models import Author, Book, Comment, Exchange

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 МБ


class BookListView(ListView):
    model = Book
    template_name = "core/index.html"
    context_object_name = "books"
    ordering = ("-name",)


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "core/add_book.html"

    def form_valid(self, form: BookForm) -> HttpResponse:
        img = form.cleaned_data["image"]
        if img and img.size > MAX_IMAGE_SIZE:
            form.add_error(
                "image", "Размер изображения не должен превышать 2 МБ"
            )
            return self.form_invalid(form)
        author = Author.objects.create(name=form.cleaned_data["author"])
        form.instance.author = author
        form.instance.owner = self.request.user
        form.instance.image = img
        self.object = form.save()
        messages.success(self.request, "Книга успешно добавлена")
        return HttpResponseRedirect(self.get_success_url())


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "my_url": reverse("core:about"),
    }

    return render(request, "core/about.html", context)


class BookDetailView(DetailView):
    model = Book
    template_name = "core/book_detail.html"
    context_object_name = "book"
    pk_url_kwarg = "book_id"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


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


class EditBookView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "core/edit_book.html"
    pk_url_kwarg = "book_id"

    def test_func(self) -> bool:
        book = self.get_object()
        return (
            self.request.user == book.owner or self.request.user.is_superuser
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
