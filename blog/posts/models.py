from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    post_date = models.DateField(auto_now=True)

    tags = models.ManyToManyField(Tag, related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('posts:user-articles', kwargs={
                       'author': self.author})

    def edit_absolute_url(self):
        return reverse('posts:edit', kwargs={'pk': self.id, 'author': self.author})

    def del_absolute_url(self):
        return reverse('cabinet:del_obj', kwargs={'pk': self.id})
