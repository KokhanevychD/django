from django.urls import path
from home.views import home_view, permission_redirect, signup


app_name = 'home'
urlpatterns = [
    path('', home_view, name='home'),
    path('fail/', permission_redirect, name='redirect'),
    path('signup/', signup, name='signup'),
]
