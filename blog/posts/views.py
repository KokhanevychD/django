from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from posts.models import Article, Tag
from posts.forms import ArticleForm
from django.urls import reverse_lazy
from django.db.models import Q


class ArticleList(ListView):
    model = Article
    context_object_name = 'obj_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Articles'
        return context

    paginate_by = 3


class UserArticleList(ListView):
    model = User
    context_object_name = 'obj_list'

    def get_queryset(self):
        self.user = User.objects.get(username=self.kwargs['author'])
        return self.user.author.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.user
        return context

    paginate_by = 3


class TagArticleList(ListView):
    model = Tag
    context_object_name = 'obj_list'

    def get_queryset(self):
        self.tag = Tag.objects.get(name=self.kwargs['tag'])
        return self.tag.articles.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.tag
        return context

    paginate_by = 3


class ArticleSearchView(ListView):
    model = Article
    context_object_name = 'obj_list'

    def get_queryset(self):
        self.search = self.request.GET.get('srch')
        return self.model.objects.filter(
                    Q(title__icontains=self.search) | Q(content__icontains=self.search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.search
        return context

    paginate_by = 3


class ArticleCreare(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:articles')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Article'
        return context


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:articles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Article'
        return context
