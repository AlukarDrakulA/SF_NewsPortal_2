from django.urls import path, include
# Импортируем созданное нами представление
from .views import NewDetail, NewsCreate, NewsList, NewsUpdate, NewsDelete, ProfileEdit

urlpatterns = [
   path('', NewsList.as_view(),  name='news_list'),
   path('<int:pk>', NewDetail.as_view(), name='news_detail'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('profile/', ProfileEdit.as_view(), name='profile_edit'),
   path('sign/', include('sign.urls')),
]