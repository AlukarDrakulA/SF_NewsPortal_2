from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory, Category, User
from django.shortcuts import redirect
from django.core.mail import send_mail

@receiver(m2m_changed, sender=PostCategory)
def notify_new_post_category(sender, instance, **kwargs):
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
    return redirect('/news_list/')