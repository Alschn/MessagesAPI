from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.status import HTTP_200_OK

from rest_framework.test import APIClient


class AuthViewsTests(TestCase):
    AUTH_URL = 'http://127.0.0.1:8000/api/auth'

    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username='test', password='testing123')

    def test_register_user(self):
        response = self.client.post(f'{self.AUTH_URL}/register/', data={
            'username': 'Tester',
            'password': 'testing123',
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsNotNone(User.objects.get(username='Tester'))

    def test_get_token(self):
        response = self.client.post(f'{self.AUTH_URL}/token/', data={
            'username': 'test',
            'password': 'testing123',
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

    def test_refresh_token(self):
        res = self.client.post(f'{self.AUTH_URL}/token/', data={
            'username': 'test',
            'password': 'testing123',
        }).json()
        access, refresh = res['access'], res['refresh']

        response = self.client.post(f'{self.AUTH_URL}/token/refresh/', data={
            'refresh': refresh
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = response.json()
        self.assertIn('access', data)
        self.assertNotEqual(access, data['access'])
