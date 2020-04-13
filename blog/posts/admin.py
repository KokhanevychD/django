from django.contrib import admin
from posts.models import Article, Tag


admin.site.register(Article)
admin.site.register(Tag)
