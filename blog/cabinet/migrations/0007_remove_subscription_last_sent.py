# Generated by Django 3.0.5 on 2020-05-21 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0006_subscription_last_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='last_sent',
        ),
    ]
