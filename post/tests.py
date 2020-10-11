import datetime
import json

from core.test_utils import IAPITestCase
from post.models import Post


class UserAppIntegrationTest(IAPITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy postów -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_create_post_valid_data(self):
        self.client.force_authenticate(user=self.test_user)
        posts_count = Post.objects.all().count()
        data = {
            'title': 'Post testowy',
            'owner': self.test_user,
            'content': 'Treść posta testowego',
            'date_posted': datetime.datetime.now()
        }
        response = self.client.post('/posts/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.all().count(), posts_count + 1)

    def test_post_create_invalid_data(self):
        self.client.force_authenticate(user=self.test_user)
        posts_count = Post.objects.all().count()
        data = {
            'title': ' ',
            'owner': self.test_user,
            'content': 'Treść posta testowego',
            'date_posted': datetime.datetime.now()
        }
        response = self.client.post('/posts/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Post.objects.all().count(), posts_count)

    def test_update_post_valid_data(self):
        self.client.force_authenticate(user=self.test_user)
        update_data = {
            'title': 'Testowy post'
        }
        response = self.client.patch('/posts/{}/'.format(self.test_post2.id), data=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('title'), 'Testowy post')

    def test_update_post_invalid_data(self):
        self.client.force_authenticate(user=self.test_user)
        update_data = {
            'title': ' '
        }
        response = self.client.patch('/posts/{}/'.format(self.test_post2.id), data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_update_post_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        update_data = {
            'title': 'Testowy post'
        }
        response = self.client.patch('/posts/{}/'.format(self.test_post.id), data=update_data)
        self.assertEqual(response.status_code, 403)

    def test_valid_get_post_list(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)

    def test_get_post_list_unauthorized(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 401)

    def test_valid_get_post(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/posts/{}/'.format(self.test_post.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('id'), self.test_post.id)

    def test_invalid_get_post(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/posts/{}/'.format(99))
        self.assertEqual(response.status_code, 404)

    def test_valid_delete_post(self):
        self.client.force_authenticate(user=self.test_user)
        posts_count = Post.objects.all().count()
        response = self.client.delete('/posts/{}/'.format(self.test_post2.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.all().count(), posts_count - 1)

    def test_invalid_delete_post(self):
        self.client.force_authenticate(user=self.test_admin)
        posts_count = Post.objects.all().count()
        response = self.client.delete('/posts/{}/'.format(99))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.all().count(), posts_count)

    def test_delete_post_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        posts_count = Post.objects.all().count()
        response = self.client.delete('/posts/{}/'.format(self.test_post.id))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.all().count(), posts_count)

