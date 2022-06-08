from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from datetime import datetime

from .models import Category, Post, User

from celery import shared_task

# import time

@shared_task
def week_sender():
    for category in Category.objects.all():
        news_from_categories = []
        week_number_last = datetime.now().isocalendar()[1] - 1
        for news in Post.objects.filter(postCategory=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'postCategory__name'):
            date_format = news.get("dateCreation").strftime("%m/%d/%Y")
            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Категория: {news.get("postCategory__name")}, Дата создания: {date_format}')
            news_from_categories.append(new)
        subscribers = category.subscribe.all()

        for subscriber in subscribers:
            html_content = render_to_string(
                'week_sender.html', {'user': subscriber,
                                     'text': news_from_categories,
                                     'category_name': category.name,
                                     'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='alastor91@mail.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')

            msg.send()
            print('Weekly sender id DONE!')

@shared_task
def notify_new_post_category(post_id):
    instance = Post.objects.get(id=post_id)
    for cat_id in instance.postCategory.all():
        users = Category.objects.filter(pk=cat_id.id).values('subscribe')
        for user_id in users:
            # email_list = [e for e in User.objects.get(pk=user_id['subscribe']).email]            
            send_mail(
                subject=f'{instance.title}',
                message=f"Здравствуй, {User.objects.get(pk=user_id['subscribe']).username}!"
                        f"Новая статья в твоем любимом разделе!\nЗаголовок статьи: {instance.title}"
                        f"Текст статьи: {instance.post[:50]} ..."
                        f"Полный текст по ссылке: http://127.0.0.1:8000/news/{instance.id}",
                from_email='alastor91@mail.ru',
                recipient_list = [User.objects.get(pk=user_id['subscribe']).email]
                )
    # return HttpResponse('email sended')
    # return redirect('/news_list/')


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")

# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)