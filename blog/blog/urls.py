from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('articles/', include('posts.urls', namespace='posts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cabinet/', include('cabinet.urls', namespace='cabinet'))
]
