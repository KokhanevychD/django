from django.http import HttpResponse
from django.shortcuts import redirect


def supreuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home:redirect')
        return view_func(request, *args, **kwargs)
    return wrapper