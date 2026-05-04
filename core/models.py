from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    publish_year = models.PositiveIntegerField(null=False, blank=False)
    annotation = models.TextField(blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books"
    )
    image = models.ImageField(upload_to="book_images/", null=True, blank=True)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="books"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("name",)

    def __str__(self) -> str:
        return f'{self.author}: "{self.name}"'
