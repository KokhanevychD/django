from django.urls import path
from posts.views import (
            article_list_view,
            article_create_view,
            article_edit_view,
            article_search,
            )


app_name = 'posts'
urlpatterns = [
    path('', article_list_view, name='articles'),
    path('<str:user_name>', article_list_view, name='user-articles'),
    path('new/', article_create_view, name='create'),
    path('edit/<str:author>/<int:id>', article_edit_view, name='edit'),
    path('search/', article_search, name='search'),
    path('tags/<str:tag>', article_list_view, name='tag'),
]
