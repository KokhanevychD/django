from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render


class SignUp(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('login')


def home_view(request, permission_check=None):

    context = {'title': 'My blog'}
    return render(request, 'base.html', context)


def permission_redirect(request):
    context = {
        'title': 'My blog',
        'message': 'Permission denied',
    }
    return render(request, 'base.html', context)
