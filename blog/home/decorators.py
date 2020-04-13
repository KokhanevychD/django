from django.http import HttpResponse
from django.shortcuts import redirect


def not_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('cabinet:cabinet')
        return view_func(request, *args, **kwargs)
    return wrapper