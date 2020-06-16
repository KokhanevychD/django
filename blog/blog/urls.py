from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import include, path

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cabinet/', include('cabinet.urls', namespace='cabinet')),
    path('api/', include('api.urls', namespace='api')),
    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
