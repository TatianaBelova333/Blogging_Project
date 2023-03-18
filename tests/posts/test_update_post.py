import random
from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from posts.models import Post
from tests.factories import PostFactory, UserFactory


class TestPostUpdate(TestCase):
    """PostUpdateView test suite"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = PostFactory()
        cls.user = cls.post.author
        cls.another_user = UserFactory(username="another_user")
        cls.admin = UserFactory(is_staff=True)
        cls.url = f"/posts/{cls.post.pk}/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestPostUpdate.user)

        self.authorized_another_user = APIClient()
        self.authorized_another_user.force_login(TestPostUpdate.another_user)

        self.authorized_admin = APIClient()
        self.authorized_admin.force_login(TestPostUpdate.admin)

    def test_update_post_by_authorised_author(self):
        """Updating a post by an authorised post author with valid data."""
        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }
        response = self.authorized_client.patch(
            path=TestPostUpdate.url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Post.objects.filter(
                pk=TestPostUpdate.post.pk,
                title=data['title'],
                text=data["text"],
                author=TestPostUpdate.user,
            ).exists()
        )

    def test_update_post_by_unauthorised(self):
        """Updating a single post by an unauthorised user."""
        post_to_update = TestPostUpdate.post
        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }
        response = self.guest_client.patch(
            path=TestPostUpdate.url,
            data=data,
            format='json',
        )
        post_attempted_update = Post.objects.get(pk=post_to_update.pk)
        data = (
            (post_to_update.text, post_attempted_update.text),
            (post_to_update.title, post_attempted_update.title),
            (post_to_update.created, post_attempted_update.created),
            (post_to_update.updated, post_attempted_update.updated),
            (post_to_update.author, post_attempted_update.author)
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        for post_to_update, post_attempted_update in data:
            with self.subTest(post_to_update=post_to_update,
                              post_attempted_update=post_attempted_update):
                self.assertEqual(post_to_update, post_attempted_update)

    def test_update_post_by_admin(self):
        """Updating a single post by an admin user."""
        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }
        response = self.authorized_admin.patch(
            path=TestPostUpdate.url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Post.objects.filter(
                pk=TestPostUpdate.post.pk,
                title=data['title'],
                text=data["text"],
                author=TestPostUpdate.user,
            ).exists()
        )

    def test_update_post_by_another_user(self):
        """Updating a single post by not post author."""
        post_to_update = TestPostUpdate.post
        data = {
            "title": "Тестовый заголовок",
            "text": "Тестовый пост",
        }
        response = self.authorized_another_user.patch(
            path=TestPostUpdate.url,
            data=data,
            format='json',
        )
        post_attempted_update = Post.objects.get(pk=post_to_update.pk)
        data = (
            (post_to_update.text, post_attempted_update.text),
            (post_to_update.title, post_attempted_update.title),
            (post_to_update.created, post_attempted_update.created),
            (post_to_update.updated, post_attempted_update.updated),
            (post_to_update.author, post_attempted_update.author)
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        for post_to_update, post_attempted_update in data:
            with self.subTest(post_to_update=post_to_update,
                              post_attempted_update=post_attempted_update):
                self.assertEqual(post_to_update, post_attempted_update)

    def test_update_post_title_with_forbidden_words(self):
        """
        Updating a post by an authorised post author with title containing forbidden words.

        """
        post = TestPostUpdate.post
        forbidden_words = settings.FORBIDDEN_WORDS

        data = {
            "title": f"Тестовый {random.choice(forbidden_words)}",
        }

        response = self.authorized_client.patch(
            path=TestPostUpdate.url,
            data=data,
            format='json',
        )
        expected_response_data = {
            'title': [ErrorDetail(
                string=f"Заголовок не должен содержать следующие слова: {', '.join(forbidden_words)}",
                code='invalid')]
        }
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(post.title, Post.objects.get(pk=post.pk).title)
