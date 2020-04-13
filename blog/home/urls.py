from django.urls import path
from home.views import home_view, permission_redirect, SignUp
from home.decorators import not_authenticated


app_name = 'home'
urlpatterns = [
    path('', home_view, name='home'),
    path('fail/', permission_redirect, name='redirect'),
    path('signup/', not_authenticated(SignUp.as_view()), name='signup'),
]
