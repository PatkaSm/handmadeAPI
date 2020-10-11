import json
from django.urls import reverse
from core.test_utils import IAPITestCase
from user.models import User


class UserAppIntegrationTest(IAPITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy panelu użytkownika -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.basic_data = {'password': 'testPassword',
                          'first_name': 'Testowy',
                          'last_name': 'Testowy',
                          'nickname': 'TestowyNick'}

    def test_register_endpoint_proper_data(self):
        users_count = User.objects.all().count()
        data = {
            'email': 'testEmail@email.com',
            **self.basic_data
        }
        response = self.client.post('/users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.all().count(), users_count + 1)

    def test_register_endpoint_invalid_data(self):
        data = {
            'email': 'wrong_email',
            **self.basic_data
        }
        response = self.client.post('/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_profile_valid_data(self):
        self.client.force_authenticate(user=self.test_user)
        update_data = {'first_name': 'Testowy2'}
        response = self.client.patch('/users/{}/'.format(self.test_user.id), data=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('first_name'), 'Testowy2')

    def test_update_profile_invalid_data(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put('/users/{}/'.format(self.test_user.id), data={**self.basic_data, 'email': ''})
        self.assertEqual(response.status_code, 400)

    def test_update_profile_unauthorized(self):
        response = self.client.put('/users/{}/'.format(self.test_user.id), data={**self.basic_data, 'email': ''})
        self.assertEqual(response.status_code, 401)

    def test_getting_logged_user(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('user-my_profile'))
        data = json.loads(response.content)
        self.assertEqual(data.get('id'), self.test_user.id)
        self.assertEqual(response.status_code, 200)

    def test_not_getting_logged_user(self):
        response = self.client.get(reverse('user-my_profile'))
        self.assertEqual(response.status_code, 401)

    def test_valid_get_user_profile(self):
        response = self.client.get('/users/{}/'.format(self.test_user2.id))
        data = json.loads(response.content)
        self.assertEqual(data.get('id'), self.test_user2.id)
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_user_profile(self):
        response = self.client.get('/users/{}/'.format(99))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

    def test_valid_delete_user(self):
        self.client.force_authenticate(user=self.test_admin)
        users_count = User.objects.all().count()
        response = self.client.delete('/users/{}/'.format(self.test_user2.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.all().count(), users_count - 1)

    def test_invalid_delete_user(self):
        self.client.force_authenticate(user=self.test_admin)
        users_count = User.objects.all().count()
        response = self.client.delete('/users/{}/'.format(99))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(User.objects.all().count(), users_count)

    def test_delete_user_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        users_count = User.objects.all().count()
        response = self.client.delete('/users/{}/'.format(self.test_user2.id))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.all().count(), users_count)

    def test_valid_disabled_user(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.post(reverse('user-disabled_user', kwargs={'user_id': self.test_user2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.test_user.active, True)

    def test_invalid_disabled_user(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.post(reverse('user-disabled_user', kwargs={'user_id': 99}))
        self.assertEqual(response.status_code, 404)
