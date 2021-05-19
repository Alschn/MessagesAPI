import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED,
)
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Message
from api.serializers import MessageSerializer


class APIViewsTests(TestCase):
    BASE_URL = 'http://127.0.0.1:8000/api'

    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username='test', password='testing123')

    @property
    def bearer_token(self):
        """Returns Authorization headers, which can be passed to APIClient instance."""
        refresh = RefreshToken.for_user(self.user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_is_authenticated(self):
        """Test views with required authorization"""
        response = self.client.post(f'{self.BASE_URL}/messages', data={})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

        response = self.client.put(f'{self.BASE_URL}/messages/4', data={})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_list_or_create_wrong_method(self):
        """Test ListCreateAPIView with not allowed methods"""
        response = self.client.delete(f'{self.BASE_URL}/messages', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(f'{self.BASE_URL}/messages', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(f'{self.BASE_URL}/messages', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_no_messages(self):
        response = self.client.get(f'{self.BASE_URL}/messages', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_list_all_messages(self):
        Message.objects.bulk_create([
            Message(content='message1'),
            Message(content='message2'),
            Message(content='message3'),
        ])
        response = self.client.get(f'{self.BASE_URL}/messages', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_create_new_message(self):
        response = self.client.post(f'{self.BASE_URL}/messages', data={
            'content': 'Test message'
        }, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_create_empty_message(self):
        response = self.client.post(f'{self.BASE_URL}/messages', data={
            'content': ''
        }, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_create_message_160_characters(self):
        response = self.client.post(f'{self.BASE_URL}/messages', data={
            'content': ''.join(random.choice(string.ascii_letters) for i in range(160))
        }, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_create_too_long_message(self):
        response = self.client.post(f'{self.BASE_URL}/messages', data={
            'content': ''.join(random.choice(string.ascii_letters) for i in range(200))
        }, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_message_not_exists(self):
        response = self.client.get(f'{self.BASE_URL}/messages/1', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_get_message(self):
        message = Message.objects.create(content='Test')
        self.assertEqual(message.views, 0)
        response = self.client.get(f'{self.BASE_URL}/messages/{message.id}', **self.bearer_token)
        message.refresh_from_db()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), MessageSerializer(message).data)
        self.assertEqual(message.views, 1)

    def test_update_message(self):
        message = Message.objects.create(content='Test message', views=1)
        self.assertEqual(message.content, 'Test message')
        response = self.client.patch(f'{self.BASE_URL}/messages/{message.id}', data={
            'content': 'Updated message'
        }, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.content, 'Updated message')
        self.assertEqual(response.json()['views'], 0)

    def test_delete_message(self):
        Message.objects.create(content='1st message')
        m2 = Message.objects.create(content='2nd message')
        key = m2.id
        self.assertEqual(Message.objects.all().count(), 2)
        response = self.client.delete(f'{self.BASE_URL}/messages/{key}', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.all().count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Message.objects.get(id=key)

    def test_get_update_delete_no_id_given(self):
        response = self.client.get(f'{self.BASE_URL}/messages/', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        response = self.client.put(f'{self.BASE_URL}/messages/', data={}, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        response = self.client.patch(f'{self.BASE_URL}/messages/', data={}, **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        response = self.client.delete(f'{self.BASE_URL}/messages/', **self.bearer_token)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
