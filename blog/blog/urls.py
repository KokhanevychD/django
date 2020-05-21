from django.contrib import admin
from django.urls import path, include
from blog import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('articles/', include('posts.urls', namespace='posts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cabinet/', include('cabinet.urls', namespace='cabinet')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
