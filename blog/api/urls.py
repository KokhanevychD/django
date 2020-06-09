from django.urls import path

from api.views import (ArtListCreateAPI,
                       ArtRetrieveUpdateDestroyAPI,
                       AvatarListCreateAPI,
                       AvatarRetrieveUpdateDestroyAPI,
                       SubListCreateAPI,
                       SubRetrieveUpdateDestroyAPI,
                       TagListCreateAPI,
                       TagRetrieveUpdateDestroyAPI,)


app_name = 'api'

urlpatterns = [
    path('articles/', ArtListCreateAPI.as_view(), name='article-list'),
    path('articles/<int:pk>',
         ArtRetrieveUpdateDestroyAPI.as_view(), name='article-detail'),
    path('avatars/', AvatarListCreateAPI.as_view(), name='avatar-list'),
    path('avatars/<int:pk>',
         AvatarRetrieveUpdateDestroyAPI.as_view(), name='avatar-detail'),
    path('subscriptions/',
         SubListCreateAPI.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>',
         SubRetrieveUpdateDestroyAPI.as_view(), name='subscription-detail'),
    path('tags/', TagListCreateAPI.as_view(), name='tag-list'),
    path('tags/<int:pk>',
         TagRetrieveUpdateDestroyAPI.as_view(), name='tag-detail'),
]
