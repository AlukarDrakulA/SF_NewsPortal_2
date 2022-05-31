from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime

from .models import Category, Post

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