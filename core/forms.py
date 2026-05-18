from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import Author, Book, Comment


class AddBookForm(forms.Form):
    name = forms.CharField(
        max_length=256,
        required=True,
        label="Название книги",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    publish_year = forms.IntegerField(
        required=True,
        label="Год публикации",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    annotation = forms.CharField(
        required=False,
        label="Аннотация",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    author = forms.CharField(
        max_length=256,
        required=True,
        label="Автор",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    image = forms.ImageField(
        required=False,
        label="Обложка",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "publish_year", "annotation", "author", "image"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "publish_year": forms.NumberInput(attrs={"class": "form-control"}),
            "annotation": forms.Textarea(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {  # noqa: RUF012
            "name": "Название книги",
            "publish_year": "Год публикации",
            "annotation": "Аннотация",
            "author": "Автор",
            "image": "Обложка",
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        widgets = {  # noqa: RUF012
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {  # noqa: RUF012
            "name": "Имя автора",
        }
        fields = ["name"]  # noqa: RUF012


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
