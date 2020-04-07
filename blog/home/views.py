from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home_view(request, permission_check=None):

    context = {'title': 'My blog'}
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})


def permission_redirect(request):
    context = {
        'title': 'My blog',
        'message': 'Permission denied',
    }
    return render(request, 'home.html', context)
