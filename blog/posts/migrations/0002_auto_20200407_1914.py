# Generated by Django 3.0.4 on 2020-04-07 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='articles', to='posts.Tag'),
        ),
    ]
