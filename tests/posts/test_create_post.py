import random
from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from posts.models import Post
from tests.factories import UserFactory

URL = "/posts/"


class TestPostCreate(TestCase):
    """PostCreateView test suite"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.under_age_user = UserFactory(birthday=datetime(2020, 1, 1))

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestPostCreate.user)

        self.authorized_under_age_user = APIClient()
        self.authorized_under_age_user.force_login(
            TestPostCreate.under_age_user
        )

    def test_create_post_success(self):
        """Creating a new post by an authorised user with valid data."""
        post_count = Post.objects.count()
        start_time = timezone.now()

        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }

        response = self.authorized_client.post(
            path=URL,
            data=data,
            format='json',
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                title=data['title'],
                text=data["text"],
                author=TestPostCreate.user,
                created__range=(start_time, timezone.now()),
                updated__range=(start_time, timezone.now()),
            ).exists()
        )

    def test_create_post_under_age_user(self):
        """Creating a new post by an authorised user with valid data."""
        post_count = Post.objects.count()
        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }

        response = self.authorized_under_age_user.post(
            path=URL,
            data=data,
            format='json',
        )
        expected_response_data = {
            'detail': ErrorDetail(
                string='Добавлять посты могут пользователи старше 18',
                code='permission_denied')
        }
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(response.data, expected_response_data)
        self.assertFalse(
            Post.objects.filter(
                title=data['title'],
                text=data["text"],
                author=TestPostCreate.under_age_user,
            ).exists()
        )

    def test_create_post_unauthorised(self):
        """Creating a new post by an unauthorised user with valid data."""
        post_count = Post.objects.count()
        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }

        response = self.guest_client.post(
            path=URL,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertFalse(
            Post.objects.filter(
                title=data['title'],
                text=data["text"],
            ).exists()
        )

    def test_create_post_title_with_forbidden_words(self):
        """Creating a new post by an unauthorised user with valid data."""
        forbidden_words = settings.FORBIDDEN_WORDS
        post_count = Post.objects.count()

        data = {
            "title": f"Тестовый {random.choice(forbidden_words)}",
            "text": "Тестовый пост",
        }

        response = self.authorized_client.post(
            path=URL,
            data=data,
            format='json',
        )
        expected_response_data = {
            'title': [ErrorDetail(
                string=f"Заголовок не должен содержать следующие слова: {', '.join(forbidden_words)}",
                code='invalid')]
        }

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(response.data, expected_response_data)
        self.assertFalse(
            Post.objects.filter(
                title=data['title'],
                text=data["text"],
            ).exists()
        )