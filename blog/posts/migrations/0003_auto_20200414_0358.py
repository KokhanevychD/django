# Generated by Django 3.0.4 on 2020-04-14 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200407_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-post_date']},
        ),
    ]
