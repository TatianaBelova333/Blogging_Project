from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Post, Comment
from tests.factories import UserFactory, PostFactory, CommentFactory
from users.models import User


class TestUserDelete(TestCase):
    """Test suite for deleting a single user."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.admin = UserFactory(is_staff=True)
        cls.url = f"/users/{cls.user.pk}/"
        PostFactory.create_batch(size=5, author=cls.user)
        CommentFactory.create_batch(size=5, author=cls.user)

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestUserDelete.user)

        self.authorized_admin = APIClient()
        self.authorized_admin.force_login(TestUserDelete.admin)

    def test_delete_user_by_admin(self):
        """Test that an admin can delete a specific user and
        the user's comments and posts will be deleted automatically.

        """
        user_to_delete = TestUserDelete.user
        response = self.authorized_admin.delete(path=TestUserDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(
            User.objects.filter(pk=user_to_delete.pk).exists()
        )
        self.assertFalse(Post.objects.filter(author=user_to_delete.pk).all())
        self.assertFalse(Comment.objects.filter(author=user_to_delete.pk).all())

    def test_delete_user_by_authorised_user(self):
        """Test for deleting a single user by the authorised user being this user."""
        user_to_delete = TestUserDelete.user
        response = self.authorized_client.delete(path=TestUserDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(
            User.objects.filter(pk=user_to_delete.pk).exists()
        )

    def test_delete_user_by_unauthorised_user(self):
        """Test for deleting a single user by an unauthorised user."""
        user_to_delete = TestUserDelete.user
        response = self.guest_client.delete(path=TestUserDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertTrue(
            User.objects.filter(pk=user_to_delete.pk).exists()
        )

