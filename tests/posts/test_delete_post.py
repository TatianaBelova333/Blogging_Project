from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Comment, Post
from tests.factories import UserFactory, PostFactory, CommentFactory


class TestPostDelete(TestCase):
    """Test suite for deleting a single post."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = PostFactory()
        cls.user = cls.post.author

        cls.url = f"/posts/{cls.post.pk}/"
        CommentFactory.create_batch(size=5, post=cls.post)

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(UserFactory(username="another_user"))

        self.authorized_post_author = APIClient()
        self.authorized_post_author.force_login(TestPostDelete.user)

        self.authorized_admin = APIClient()
        self.authorized_admin.force_login(UserFactory(is_staff=True))

    def test_delete_post_by_unauthorised_user(self):
        """Test that an unauthorised user cannot delete any post."""
        post_to_delete = TestPostDelete.post
        response = self.guest_client.delete(path=TestPostDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertTrue(
            Post.objects.filter(pk=post_to_delete.pk).exists()
        )

    def test_delete_post_by_authorised_not_author(self):
        """
        Test that an authorised user cannot delete other users' posts.

         """
        post_to_delete = TestPostDelete.post
        response = self.authorized_client.delete(path=TestPostDelete.url)
        self.assertTrue(
            Post.objects.filter(pk=post_to_delete.pk).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_post_by_post_author(self):
        """Test that an authorised post author can delete their posts and
        the related post comments will be deleted automatically.

        """
        post_to_delete = TestPostDelete.post
        response = self.authorized_post_author.delete(path=TestPostDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(
            Post.objects.filter(pk=post_to_delete.pk).exists()
        )
        self.assertFalse(
            Comment.objects.filter(post=post_to_delete.pk).all()
        )

    def test_delete_post_by_admin(self):
        """Test that an admin can delete other users' posts and
        the related post comments will be deleted automatically.

        """
        post_to_delete = TestPostDelete.post
        response = self.authorized_admin.delete(path=TestPostDelete.url)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(
            Post.objects.filter(pk=post_to_delete.pk).exists()
        )
        self.assertFalse(
            Comment.objects.filter(post=post_to_delete.pk).all()
        )
