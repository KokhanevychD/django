from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from cabinet.forms import AvatarForm
from cabinet.models import Subscription
from posts.models import Article, Tag
from posts.forms import TagForm


class CabinetListView(ListView):
    model = Article
    template_name = 'cabinet/cabinet.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            user = User.objects.get(username=self.request.user)
            return user.author.all()
        else:
            return Article.objects.all()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        self.user = User.objects.get(username=self.request.user)
        context['title'] = self.request.user
        context['cabinet'] = f'This is {self.request.user} cabinet'
        try:
            context['avatar'] = self.user.avatar.avatar
        except:
            pass

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Tag'
        return context


class UploadAvatar(CreateView):
    form_class = AvatarForm
    template_name = 'cabinet/user_avatar.html'
    success_url = reverse_lazy('cabinet:cabinet')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CreateSubscription(CreateView):
    model = Subscription
    fields = ['author_sub']
    template_name = 'posts/create.html'
    success_url = reverse_lazy('cabinet:cabinet')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class UpdateSubscription(UpdateView):
    model = Subscription
    template_name = 'posts/create.html'
    fields = ['author_sub']
    success_url = reverse_lazy('cabinet:cabinet')