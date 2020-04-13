from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.models import User
from posts.models import Article, Tag
from posts.forms import TagForm
from django.urls import reverse_lazy


class CabinetListView(ListView):
    model = Article
    context_object_name = 'obj_list'
    template_name = 'cabinet/cabinet.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            user = User.objects.get(username=self.request.user)
            return user.author.all()
        else:
            return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user
        context['cabinet'] = f'This is {self.request.user} cabinet'
        return context

    paginate_by = 3


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('cabinet:cabinet')


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('cabinet:cabinet')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Tag'
        return context
