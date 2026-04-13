from django import forms


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
