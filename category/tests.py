import json

from django.urls import reverse

from category.models import Category
from core.test_utils import IAPITestCase
from tag.models import Tag


class UserAppIntegrationTest(IAPITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy kategorii -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_create_category_valid_data(self):
        self.client.force_authenticate(user=self.test_admin)
        categories_count = Category.objects.all().count()
        data = {
            'name': 'Kategoria testowa',
            'parent': self.test_category3.id,
            'img': '',
        }
        response = self.client.post(reverse('category-create_category'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.all().count(), categories_count + 1)

    def test_category_create_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        data = {
            'name': 'Kategoria testowa',
            'parent': self.test_category3.id,
            'img': '',
        }
        response = self.client.post(reverse('category-create_category'), data=data)
        self.assertEqual(response.status_code, 403)

    def test_category_create_invalid_data(self):
        self.client.force_authenticate(user=self.test_admin)
        data = {
            'name': ' ',
            'parent': self.test_category3,
            'img': '',
        }
        response = self.client.post(reverse('category-create_category'), data=data)
        self.assertEqual(response.status_code, 406)

    def test_update_category_valid_data(self):
        self.client.force_authenticate(user=self.test_admin)
        update_data = {'name': 'Kategoria testowa2'}
        response = self.client.put(reverse('category-update_category', kwargs={'category_id': self.test_category3.id}),
                                   data=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('category')['name'], 'Kategoria testowa2')

    def test_update_category_invalid_data(self):
        self.client.force_authenticate(user=self.test_admin)
        update_data = {'name': ''}
        response = self.client.put(reverse('category-update_category', kwargs={'category_id': self.test_category3.id}),
                                   data=update_data)
        self.assertEqual(response.status_code, 406)

    def test_update_category_unauthorized(self):
        update_data = {'name': 'Kategoria testowa2'}
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put(reverse('category-update_category', kwargs={'category_id': self.test_category3.id}),
                                   data=update_data)
        self.assertEqual(response.status_code, 403)

    def test_valid_get_nav_categories(self):
        response = self.client.get(reverse('category-nav_categories'))
        self.assertEqual(response.status_code, 200)

    def test_valid_get_categories_to_add_offer(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('category-categories_to_add_offer'))
        self.assertEqual(response.status_code, 200)

    def test_valid_get_categories_to_add_offer_unauthorized(self):
        response = self.client.get(reverse('category-categories_to_add_offer'))
        self.assertEqual(response.status_code, 401)

    def test_valid_get_category(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get('/categories/{}/'.format(self.test_category3.id))
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_category(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get('/categories/{}/'.format(99))
        self.assertEqual(response.status_code, 404)

    def test_get_category_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/categories/{}/'.format(self.test_category3.id))
        self.assertEqual(response.status_code, 403)

    def test_valid_delete_category(self):
        self.client.force_authenticate(user=self.test_admin)
        categories_count = Category.objects.all().count()
        response = self.client.delete('/categories/{}/'.format(self.test_category3.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.all().count(), categories_count - 1)

    def test_invalid_delete_category(self):
        self.client.force_authenticate(user=self.test_admin)
        categories_count = Category.objects.all().count()
        response = self.client.delete('/categories/{}/'.format(99))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tag.objects.all().count(), categories_count)

    def test_delete_category_unauthorized(self):
        self.client.force_authenticate(user=self.test_user)
        categories_count = Category.objects.all().count()
        response = self.client.delete('/categories/{}/'.format(self.test_category2.id))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Category.objects.all().count(), categories_count)
