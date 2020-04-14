# from django.forms import ModelForm
from django import forms
from posts.models import Article, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'tags',
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
