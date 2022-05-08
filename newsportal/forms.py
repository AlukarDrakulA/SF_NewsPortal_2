from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = [
            'author',
            'categoryType',
            'postCategory',
            'title',
            'post',
       ]


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        post = cleaned_data.get("post")

        if title == post:
            raise ValidationError(
                "Содержание поста не должно быть идентично названию."
            )

        return cleaned_data