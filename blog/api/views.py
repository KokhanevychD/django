from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from api.permissions import AuthorOrAdmin, UserOrAdmin
from api.serializers import (ArticlePOSTSerializer, ArticleSerializer,
                             AvatarSerializer, AvatarPOSTSerializer,
                             SubscriptionPOSTSerializer,
                             SubscriptionSerializer, TagSerializer,
                             )

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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AvatarPOSTSerializer
        return AvatarSerializer


class AvatarRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Avatar.objects.all()
    permission_classes = [UserOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return AvatarPOSTSerializer
        return AvatarSerializer


class SubListCreateAPI(ListCreateAPIView):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubscriptionPOSTSerializer
        return SubscriptionSerializer


class SubRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [UserOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubscriptionPOSTSerializer
        return SubscriptionSerializer


class TagListCreateAPI(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH', 'PUT']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
