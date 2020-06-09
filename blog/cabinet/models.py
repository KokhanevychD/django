from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='avatar')
    avatar = models.ImageField(upload_to='uploads')

    def __str__(self):
        return f'{self.user}\'s avatar'


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='sub')
    author_sub = models.ManyToManyField(User, related_name='auth_sub')

    def __str__(self):
        return f'{self.user}\'s subscription'
