from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Article, Tag


class BaseTestSetUp(APITestCase):

    def setUp(self):

        self.user, created = User.objects.get_or_create(
            username='testuser'
        )
        self.user.set_password('testpass1212')
        self.user.save()

        self.user_2, created = User.objects.get_or_create(
            username='testuser_2'
        )
        self.user_2.set_password('testpass1212')
        self.user_2.save()

        self.admin, created = User.objects.get_or_create(
            username='admin',
            is_superuser=True
        )
        self.admin.set_password('testpass1212')
        self.admin.save()

        self.tag, created = Tag.objects.get_or_create(
            name='test_tag'
        )
        self.tag.save()

        self.article, created = Article.objects.get_or_create(
            title='test article',
            content='test article',
            author=self.user,
        )
        self.article.tags.add(self.tag)
        self.article.save()

    def user_auth(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpass1212'}
        response = self.client.post(url, data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        return self.user

    def admin_auth(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'admin', 'password': 'testpass1212'}
        response = self.client.post(url, data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        return self.admin


class AuthTests(BaseTestSetUp):

    def test_auth_permissions(self):
        url = reverse('api:article-list')
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_auth_fail_permissinons(self):
        url = reverse('api:article-list')
        self.client.credentials(HTTP_AUTHORIZATION=None)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)


class ArticlesTests(BaseTestSetUp):

    def test_get_list_article(self):
        url = reverse('api:article-list')
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_post_article(self):
        url = reverse('api:article-list')
        tag_pk = self.tag.pk
        self.user_auth()
        data = {
            'title': 'test article',
            'content': 'test content',
            'tags': [tag_pk]
        }
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_fail_post_article(self):
        url = reverse('api:article-list')
        tag_pk = self.tag.pk
        self.user_auth()
        data = {
            'title': '',
            'content': 'test content',
            'tags': [tag_pk]
        }
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_article(self):
        pk = self.article.pk
        url = reverse('api:article-detail', kwargs={'pk': pk})
        title = 'test article update'
        data = {
            'title': title
        }
        self.user_auth()
        responce = self.client.patch(url, data)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        obj = Article.objects.get(pk=pk)
        self.assertEqual(obj.title, title)

    def test_author_del_article(self):
        article = Article.objects.create(
            title='test article for del',
            content='test article',
            author=self.user,
        )
        article.save()
        pk = article.pk
        url = reverse('api:article-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
        obj_check = Article.objects.filter(pk=pk)
        self.assertEqual(obj_check.count(), 0)

    def test_admin_del_article(self):
        article = Article.objects.create(
            title='test article for del',
            content='test article',
            author=self.user,
        )
        article.save()
        pk = article.pk
        url = reverse('api:article-detail', kwargs={'pk': pk})
        self.admin_auth()
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
        obj_check = Article.objects.filter(pk=pk)
        self.assertEqual(obj_check.count(), 0)

    def test_del_no_permission_article(self):
        article = Article.objects.create(
            title='test article for del',
            content='test article',
            author=self.user,
        )
        article.save()
        pk = article.pk
        url = reverse('api:article-detail', kwargs={'pk': pk})
        self.client.force_authenticate(user=self.user_2)
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_article(self):
        pk = self.article.pk
        url = reverse('api:article-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.data['content'], self.article.content)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
