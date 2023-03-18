from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Post
from tests.factories import UserFactory, PostFactory


class TestPostList(TestCase):
    """Test suite for retrieving a list of posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        PostFactory.create_batch(size=10)
        cls.user = UserFactory()
        cls.url = "/posts/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestPostList.user)

    def test_user_list_authorised(self):
        """Test for retrieving a list of posts by an authorised user."""
        response = self.authorized_client.get(path=TestPostList.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Post.objects.count())

    def test_user_list_unauthorised(self):
        """Test for retrieving a list of posts by an unauthorised user."""
        response = self.guest_client.get(path=TestPostList.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Post.objects.count())
