import json

from core.test_utils import IAPITestCase
from item.models import Item


class UserAppIntegrationTest(IAPITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy itemów -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_create_item_valid_data(self):
        self.client.force_authenticate(user=self.test_user)
        items_count = Item.objects.all().count()
        data = {
            'name': 'Itemek testowy',
            'category': self.test_category3.id,
            'color': 'red',
            'ready_in': 'now'
        }
        response = self.client.post('/items/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.all().count(), items_count + 1)

    def test_itm_create_invalid_data(self):
        self.client.force_authenticate(user=self.test_user)
        data = {
            'name': 'Itemek testowy',
            'category': self.test_category3.id,
            'color': 'red',
            'ready_in': 'invalid data'
        }
        response = self.client.post('/items/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_item_valid_data(self):
        update_data = {'ready_in': 'week'}
        response = self.client.patch('/items/{}/'.format(self.test_item.id), data=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('ready_in'), 'week')

    def test_update_item_invalid_data(self):
        update_data = {'ready_in': 'invalid'}
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put('/items/{}/'.format(self.test_tag.id), data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_valid_get_item(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/items/{}/'.format(self.test_item.id))
        data = json.loads(response.content)
        self.assertEqual(data.get('id'), self.test_item.id)
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_item(self):
        self.client.force_authenticate(user=self.test_item)
        response = self.client.get('/items/{}/'.format(99))
        self.assertEqual(response.status_code, 404)

    def test_valid_get_item_list(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_item(self):
        self.client.force_authenticate(user=self.test_user)
        items_count = Item.objects.all().count()
        response = self.client.delete('/items/{}/'.format(self.test_item2.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Item.objects.all().count(), items_count - 1)

    def test_invalid_delete_item(self):
        self.client.force_authenticate(user=self.test_user)
        items_count = Item.objects.all().count()
        response = self.client.delete('/items/{}/'.format(99))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Item.objects.all().count(), items_count)

