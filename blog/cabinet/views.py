from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from posts.models import Article


def user_page(request):
    if not request.user.is_authenticated:
        return redirect('home:redirect')
    if not request.user.is_superuser:
        user = User.objects.get(username=request.user)
        queryset = user.author.all()
    else:
        queryset = Article.objects.all()
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': request.user,
        'page_obj': page_obj,
    }
    return render(request, 'cabinet/cabinet.html', context)


def delete_view(request, id=None):
    if not request.user.is_superuser:
        return redirect('home:redirect')
    article = get_object_or_404(Article, pk=id)
    article.delete()
    return redirect('cabinet:cabinet')
