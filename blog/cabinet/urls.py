from django.urls import path
from posts.views import ArticleUpdateView
from django.contrib.auth.decorators import login_required
from cabinet.views import (CabinetListView, TagCreateView, ArticleDeleteView, UploadAvatar)
from cabinet.decorators import supreuser_required


app_name = 'cabinet'
urlpatterns = [
    path('', login_required(CabinetListView.as_view()), name='cabinet'),
    path('edit/<int:id>', supreuser_required(ArticleUpdateView.as_view()), name='edit'),
    path('<int:pk>/', supreuser_required(ArticleDeleteView.as_view()), name='del_obj'),
    path('new/tag/', supreuser_required(TagCreateView.as_view()), name='new-tag'),
    path('avatar/', UploadAvatar.as_view(), name='avatar'),
]
