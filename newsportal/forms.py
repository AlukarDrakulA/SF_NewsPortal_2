from django import forms
from django.core.exceptions import ValidationError

from .models import User, Post, Category


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'

        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     new_password = cleaned_data.post("new_password")
    #     confirm_password = cleaned_data.post("confirm_password")

    #     if new_password != confirm_password:
    #         raise ValidationError(
    #             "Пароли не совпадают!"
    #         )

    #     return cleaned_data
