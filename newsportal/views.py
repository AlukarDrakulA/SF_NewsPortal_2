from django.views.generic import ListView, DetailView
from .models import Post
from pprint import pprint

# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'