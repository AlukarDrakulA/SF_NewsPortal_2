from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm, ProfileForm
from .models import User, Post, Category, UserSubscribers
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .tasks import notify_new_post_category
# from django.http import HttpResponse
# from datetime import datetime, timedelta

from django.core.cache import cache # импортируем наш кэш

# Create your views here.
class NewsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    # * выполнение задачи для проверки работоспособности
    # def get(self, request):
    #     printer.delay(10)
    #     printer.apply_async([10], countdown = 5) # выполнение задачи через 5 секунд после ее создания
    #     printer.apply_async([10], 
    #                         eta = datetime.now() + timedelta(seconds=5)) # eta принимает datetime объект
    #     hello.delay()
    #     return HttpResponse('Hello!')


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save()
        post_id = post.id
        notify_new_post_category.delay(post_id)
        return redirect('/')



class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'profile_edit.html'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'author').exists()
        return context

    # def form_valid(self, form):
    #     form.send_password()
    #     return super().form_valid()


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_categories = Category.objects.all()
        user_subscribe_category = UserSubscribers.objects.filter(user_id = User.objects.get(id=self.request.user.id))
        
        cat_id_list = []
        cat_name_list = []

        for i in all_categories:
            cat_id_list.append(i.id)
            cat_name_list.append(i.name)
        cat_id_dict = dict(zip(cat_name_list, cat_id_list))
        
        context['cat_id'] = cat_id_dict

        cat_list = []
        for cat in all_categories:
            cat_list.append(cat.name)
        cat_user_dict = {i: False for i in cat_list}
        
        user_list = []
        for u in user_subscribe_category:
            user_list.append(str(u.category))

        for x in cat_user_dict:
            if x in user_list:
                cat_user_dict[x] = True
        
        context['subscribes'] = cat_user_dict

        return context


@login_required
def add_subscribe(request, cat):
    user = request.user
    category = Category.objects.get(name=cat)
    subscribe = UserSubscribers(user_id=user.id, category_id=category.id)
    subscribe.save()
    return redirect('/category/')


@login_required
def del_subscribe(request, cat):
    user = request.user
    category = Category.objects.get(name=cat)
    unsubscribe = UserSubscribers.objects.filter(user_id=user.id, category_id=category.id)
    unsubscribe.delete()
    return redirect('/category/')

