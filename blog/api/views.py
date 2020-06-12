from django.shortcuts import get_list_or_404

from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from api.permissions import AuthorOrAdmin, UserOrAdmin
from api.serializers import (ArticlePOSTSerializer, ArticleSerializer,
                             ArticleQuerySerializer,
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

    def get_queryset(self):
        if self.request.query_params:
            serializer = ArticleQuerySerializer(data=self.request.query_params)
            serializer.is_valid(raise_exception=True)

            if 'author' in serializer.validated_data.keys():
                usr = serializer.validated_data['author']
                self.queryset = get_list_or_404(Article, author__username=usr)

            elif 'tags' in serializer.validated_data.keys():
                tags = serializer.validated_data['tags'].split(',')
                self.queryset = get_list_or_404(Article, tags__name__in=tags)

        return self.queryset


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
