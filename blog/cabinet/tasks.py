from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from celery.task.schedules import crontab

from django.utils import timezone
from django.core.mail import send_mail

from posts.models import Article
from cabinet.models import Subscription
from blog.gmail import mail as my_mail



@periodic_task(run_every=(crontab(minute='*/1')), name='subscription_mailer')
def subscription_mailer():
    period_start = timezone.now() - timedelta(seconds=60)
    queryset = Article.objects.filter(post_date__gte=period_start)
    to_send_dict = {}
    for article in queryset:
        subscribers = Subscription.objects.filter(author_sub__username=article.author.username)
        if len(subscribers) > 0:
            for sub in subscribers:
                if str(sub.user) not in to_send_dict.keys():
                    to_send_dict[sub.user.email] = [article]
                else:
                    to_send_dict[sub.user.email].append(article)
    for mail in to_send_dict.keys():
        message = str()
        for article in to_send_dict[mail]:
            message += article.title
        send_mail('new posts from subscribed authors:',
                  message, my_mail, [mail])
    return f'receivers and articles - {to_send_dict}'
