from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User


class TestSetUp(APITestCase):
    def create_test_user(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        return res.data

    def setUp(self):
        self.token_url = reverse('get-token')
        self.register_url = reverse('user-list')
        self.user_class = User

        self.user_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()