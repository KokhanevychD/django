from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from posts.models import Article, Tag
from posts.forms import ArticleForm
from django.contrib.auth.decorators import login_required
from posts.decorators import self_author_required
from django.http import HttpResponse


def article_list_view(request, user_name=None, tag=None):

    if user_name:
        user = User.objects.get(username=user_name)
        queryset = user.author.all()
    elif tag:
        tag = Tag.objects.get(name=tag)
        queryset = tag.articles.all()
    else:
        queryset = Article.objects.all()
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Posts',
        'page_obj': page_obj,
    }
    return render(request, 'posts/posts.html', context)

@login_required
def article_create_view(request):

    article = Article(author=request.user)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        if 'cabinet' in request.path:
            return redirect('cabinet:cabinet')
        return redirect('posts:articles')
    context = {
        'title': "New post",
        'form': form,
    }
    return render(request, 'posts/create.html', context)

@self_author_required
def article_edit_view(request, id=None, author=None):
    
    article = get_object_or_404(Article, pk=id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('cabinet:cabinet')
    context = {
        'title': "Edit post",
        'form': form,
    }
    return render(request, 'posts/create.html', context)


def article_search(request):

    search = request.GET.get('srch')
    queryset = Article.objects.filter(
        Q(title__icontains=search) | Q(content__icontains=search))
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Search result',
        'page_obj': page_obj,
    }
    return render(request, 'posts/posts.html', context)
