from django.urls import path
# Импортируем созданное нами представление
from .views import NewDetail, NewsList

urlpatterns = [
   path('', NewsList.as_view()), 
   path('<int:pk>', NewDetail.as_view()),
]