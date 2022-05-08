from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gt',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    postCategory = ModelChoiceFilter(
        field_name = 'postcategory__categotyThrough',
        queryset = Category.objects.all(),
        label = 'Tags',
        empty_label = 'Любой',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }