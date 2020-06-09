import io

from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image

from rest_framework.test import APITestCase
from rest_framework import status

from cabinet.models import Avatar, Subscription
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
            is_superuser=True,
            is_staff=True,
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

        self.sub, created = Subscription.objects.get_or_create(
            user=self.user_2,
        )
        self.sub.author_sub.add(self.user)
        self.sub.save()

        self.tag, created = Tag.objects.get_or_create(name='test tag')
        self.tag.save()

    def user_auth(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpass1212'}
        response = self.client.post(url, data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        return self.user
    
    def user_2_auth(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser_2', 'password': 'testpass1212'}
        response = self.client.post(url, data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        return self.user_2

    def admin_auth(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'admin', 'password': 'testpass1212'}
        response = self.client.post(url, data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        return self.admin

    def generate_image(self):
        image_file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(image_file, format='png')
        image_file.name = 'test.png'
        image_file.seek(0)
        return image_file


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
        user = self.user_auth()
        data = {
            'title': 'test article',
            'content': 'test content',
            'tags': [tag_pk]
        }
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        art_pk = responce.data['id']
        author = Article.objects.get(pk=art_pk).author
        self.assertEqual(author.username, user.username)

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
        self.user_2_auth()
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_article(self):
        pk = self.article.pk
        url = reverse('api:article-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.data['content'], self.article.content)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)


class AvatarTests(BaseTestSetUp):

    def create_avatar(self):
        url = reverse('api:avatar-list')
        image = self.generate_image()
        user_pk = self.user.pk
        data = {
            'user': user_pk,
            'avatar': image,
        }
        self.user_auth()
        responce = self.client.post(url, data)
        return responce.data['pk']

    def test_post_avatar(self):
        url = reverse('api:avatar-list')
        image = self.generate_image()
        pk = self.user.pk
        data = {
            'user': pk,
            'avatar': image,
        }
        self.user_auth()
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_update_avatar(self):
        url_post = reverse('api:avatar-list')
        image_post = self.generate_image()
        user_pk = self.user.pk
        data_post = {
            'user': user_pk,
            'avatar': image_post,
        }
        self.user_auth()
        responce_post = self.client.post(url_post, data_post)

        pk = responce_post.data['pk']
        image = self.generate_image()
        url = reverse('api:avatar-detail', kwargs={'pk': pk})
        data = {
            'image': image
        }
        responce = self.client.patch(url, data)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_update_nopermission_avatar(self):

        pk = self.create_avatar()
        image = self.generate_image()
        self.user_2_auth()
        url = reverse('api:avatar-detail', kwargs={'pk': pk})
        data = {
            'image': image
        }
        responce = self.client.patch(url, data)
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_avatar(self):
        pk = self.create_avatar()
        url = reverse('api:avatar-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data.get('pk'), pk)

    def test_delete_avatar(self):
        pk = self.create_avatar()
        url = reverse('api:avatar-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
        obj_list = Avatar.objects.filter(pk=pk)
        self.assertEqual(obj_list.count(), 0)


class SubscriptionTests(BaseTestSetUp):

    def test_post_subscription(self):
        url = reverse('api:subscription-list')
        user = self.user_auth()
        data = {
            'author_sub': [self.user_2.pk]
        }
        responce = self.client.post(url, data)
        sub_pk = responce.data['id']
        sub = Subscription.objects.get(pk=sub_pk)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sub.user, user)
        self.assertIn(self.user_2, sub.author_sub.all())

    def test_get_detail_subscription(self):
        pk = self.sub.pk
        url = reverse('api:subscription-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        res_pk = responce.data['id']
        self.assertEqual(res_pk, pk)

    def test_update_subscription(self):        
        pk = self.sub.pk
        user_for_sub_pk = self.admin.pk
        url = reverse('api:subscription-detail', kwargs={'pk': pk})
        self.user_2_auth()
        data = {
            'author_sub': [user_for_sub_pk]
        }
        responce = self.client.patch(url, data)
        sub = Subscription.objects.get(pk=pk)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertIn(self.admin, sub.author_sub.all())

    def test_update_nopermission_subscription(self):
        # self.sub owner user is self.user_2
        pk = self.sub.pk
        user_for_sub_pk = self.admin.pk
        url = reverse('api:subscription-detail', kwargs={'pk': pk})
        self.user_auth()
        data = {
            'author_sub': [user_for_sub_pk]
            }
        responce = self.client.patch(url, data)
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    def test_del_no_permission_subscription(self):
        # self.sub owner user is self.user_2
        pk = self.sub.pk
        self.user_auth()
        url = reverse('api:subscription-detail', kwargs={'pk': pk})
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)


class TafTest(BaseTestSetUp):

    def test_post_tag(self):
        url = reverse('api:tag-list')
        self.user_auth()
        data = {
            'name': 'test'
        }
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_post_fail_tag(self):
        # each tag is unique
        url = reverse('api:tag-list')
        self.user_auth()
        name = self.tag.name
        data = {
            'name': name
        }
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_detail_tag(self):
        pk = self.tag.pk
        url = reverse('api:tag-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_delete_nopermission_tag(self):
        pk = self.tag.pk
        url = reverse('api:tag-detail', kwargs={'pk': pk})
        self.user_auth()
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tag(self):
        pk = self.tag.pk
        url = reverse('api:tag-detail', kwargs={'pk': pk})
        self.admin_auth()
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
