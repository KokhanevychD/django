from django.contrib.auth.models import User

from rest_framework import serializers

from cabinet.models import Avatar, Subscription

from posts.models import Article, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['pk', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'


class ArticlePOSTSerializer(ArticleSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionGETSerializer(SubscriptionSerializer):
    user = UserSerializer(read_only=True)
    author_sub = UserSerializer(many=True)


class AvatarSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Avatar
        fields = '__all__'
