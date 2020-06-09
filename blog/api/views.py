from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from api.permissions import AuthorOrAdmin
from api.serializers import (ArticlePOSTSerializer, ArticleSerializer,
                             AvatarSerializer, SubscriptionGETSerializer,
                             SubscriptionSerializer, TagSerializer)

from cabinet.models import Avatar, Subscription

from posts.models import Article, Tag


class ArtListCreateAPI(ListCreateAPIView):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ArticlePOSTSerializer
        return ArticleSerializer


class ArtRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = [AuthorOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ArticlePOSTSerializer
        return ArticleSerializer


class AvatarListCreateAPI(ListCreateAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


class AvatarRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


class SubListCreateAPI(ListCreateAPIView):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubscriptionGETSerializer
        return SubscriptionSerializer


class SubRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubscriptionGETSerializer
        return SubscriptionSerializer


class TagListCreateAPI(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
