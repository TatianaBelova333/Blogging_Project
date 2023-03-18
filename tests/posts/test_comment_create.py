from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Comment
from tests.factories import UserFactory, PostFactory

URL = "/comments/"


class TestCommentCreate(TestCase):
    """CommentCreateView test suite"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.post = PostFactory()

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestCommentCreate.user)

    def test_create_comment_success(self):
        """Creating a new comment by an authorised user with valid data."""
        comment_count = Comment.objects.count()
        data = {
            "text": "Тестовый комментарий",
            "post": TestCommentCreate.post.pk,
        }

        response = self.authorized_client.post(
            path=URL,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text=data["text"],
                post=data['post'],
                author=TestCommentCreate.user,
            ).exists()
        )

    def test_create_post_unauthorised(self):
        """Creating a new comment by an unauthorised user with valid data."""
        comment_count = Comment.objects.count()
        data = {
            "text": "Тестовый комментарий1",
            "post": TestCommentCreate.post.pk,
        }

        response = self.guest_client.post(
            path=URL,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), comment_count)
        self.assertFalse(
            Comment.objects.filter(
                post=data['post'],
                text=data["text"],
            ).exists()
        )