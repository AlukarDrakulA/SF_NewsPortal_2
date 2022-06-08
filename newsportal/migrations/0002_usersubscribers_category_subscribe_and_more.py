# Generated by Django 4.0.4 on 2022-05-21 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsportal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscribe',
            field=models.ManyToManyField(through='newsportal.UserSubscribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersubscribers',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsportal.category'),
        ),
        migrations.AddField(
            model_name='usersubscribers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]