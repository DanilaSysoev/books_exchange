from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Exchange(models.Model):
    pk = models.CompositePrimaryKey("book_id", "to_user_id")
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=False, blank=False)

    @property
    def duration(self) -> timezone.timedelta:  # type: ignore
        return self.return_date - self.date

    @property
    def is_active(self) -> bool:
        return self.return_date > timezone.now()


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
    received_an_exchange = models.ManyToManyField(  # type: ignore
        User, related_name="received_books", blank=True, through="Exchange"
    )

    @property
    def is_accessible_for_exchange(self) -> bool:
        all_exchanges = Exchange.objects.filter(book=self)
        return not any(exchange.is_active for exchange in all_exchanges)

    @property
    def return_date(self) -> timezone.datetime | None:  # type: ignore
        active_exchange = (
            Exchange.objects.filter(book=self).order_by("-return_date").first()
        )
        if active_exchange:
            return active_exchange.return_date
        return None

    @property
    def current_holder(self) -> User | None:
        active_exchange = (
            Exchange.objects.filter(book=self).order_by("-return_date").first()
        )
        if active_exchange and active_exchange.is_active:
            return active_exchange.to_user
        return None

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("name",)

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse("core:book_detail", kwargs={"book_id": self.pk})

    def __str__(self) -> str:
        return f'{self.author}: "{self.name}"'


class Comment(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.author} - {self.book}"
