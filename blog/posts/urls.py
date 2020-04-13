from django.urls import path
from django.contrib.auth.decorators import login_required
from posts.decorators import self_author_required
from posts.views import (
            ArticleList,
            UserArticleList,
            TagArticleList,
            ArticleSearchView,
            ArticleCreare,
            ArticleUpdateView,
            )


app_name = 'posts'
urlpatterns = [
    path('', ArticleList.as_view(), name='articles'),
    path('<str:author>', UserArticleList.as_view(), name='user-articles'),
    path('new/', login_required(ArticleCreare.as_view()), name='create'),
    path('edit/<str:author>/<int:pk>', self_author_required(ArticleUpdateView.as_view()), name='edit'),
    path('search/', ArticleSearchView.as_view(), name='search'),
    path('tags/<str:tag>', TagArticleList.as_view(), name='tag'),
]
