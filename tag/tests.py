import json

from core.test_utils import IAPITestCase
from tag.models import Tag


class UserAppIntegrationTest(IAPITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy tagów -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_create_tag_valid_data(self):
        self.client.force_authenticate(user=self.test_user)
        tags_count = Tag.objects.all().count()
        data = {
            'word': 'Tag testowy',
        }
        response = self.client.post('/tags/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.all().count(), tags_count + 1)

    def test_tag_create_invalid_data(self):
        self.client.force_authenticate(user=self.test_user)
        data = {
            'word': '',
        }
        response = self.client.post('/tags/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_tag_valid_data(self):
        self.client.force_authenticate(user=self.test_admin)
        update_data = {'word': 'Tag testowy2'}
        response = self.client.patch('/tags/{}/'.format(self.test_tag.id), data=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('word'), 'Tag testowy2')

    def test_update_tag_invalid_data(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.put('/tags/{}/'.format(self.test_tag.id), data={'word': ''})
        self.assertEqual(response.status_code, 400)

    def test_update_tag_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put('/tags/{}/'.format(self.test_tag.id), data={'word': 'Testowy tag 3'})
        self.assertEqual(response.status_code, 403)

    def test_valid_get_tag(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get('/tags/{}/'.format(self.test_tag2.id))
        data = json.loads(response.content)
        self.assertEqual(data.get('id'), self.test_tag2.id)
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_tag(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get('/tags/{}/'.format(99))
        self.assertEqual(response.status_code, 404)

    def test_get_tag_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/tags/{}/'.format(99))
        self.assertEqual(response.status_code, 403)

    def test_valid_get_tag_list(self):
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_tag(self):
        self.client.force_authenticate(user=self.test_admin)
        tags_count = Tag.objects.all().count()
        response = self.client.delete('/tags/{}/'.format(self.test_tag3.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Tag.objects.all().count(), tags_count - 1)

    def test_invalid_delete_tag(self):
        self.client.force_authenticate(user=self.test_admin)
        tags_count = Tag.objects.all().count()
        response = self.client.delete('/tags/{}/'.format(99))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tag.objects.all().count(), tags_count)

    def test_delete_tag_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        tags_count = Tag.objects.all().count()
        response = self.client.delete('/tags/{}/'.format(self.test_user2.id))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tag.objects.all().count(), tags_count)
