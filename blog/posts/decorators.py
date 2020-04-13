from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User


def self_author_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        if kwargs['author'] != str(user) and not user.is_superuser:
            return redirect('home:redirect')
        return view_func(request, *args, **kwargs)
    return wrapper
