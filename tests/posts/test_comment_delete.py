from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Comment, Post
from tests.factories import UserFactory, PostFactory, CommentFactory


class TestCommentDelete(TestCase):
    """Test suite for deleting a single comment."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.comment = CommentFactory()
        cls.user = cls.comment.author

        cls.url = f"/comments/{cls.comment.pk}/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(UserFactory(username="another_user"))

        self.authorized_comment_author = APIClient()
        self.authorized_comment_author.force_login(TestCommentDelete.user)

        self.authorized_admin = APIClient()
        self.authorized_admin.force_login(UserFactory(is_staff=True))

    def test_delete_comment_by_unauthorised_user(self):
        """Test that an unauthorised user cannot delete any comments."""
        comment_to_delete = TestCommentDelete.comment
        response = self.guest_client.delete(path=TestCommentDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertTrue(
            Comment.objects.filter(pk=comment_to_delete.pk).exists()
        )

    def test_delete_comment_by_authorised_not_author(self):
        """
        Test that an authorised user cannot delete other users' comments.

        """
        comment_to_delete = TestCommentDelete.comment
        response = self.authorized_client.delete(path=TestCommentDelete.url)
        self.assertTrue(
            Comment.objects.filter(pk=comment_to_delete.pk).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_comment_by_comment_author(self):
        """Test that an authorised comment author can delete their comments.

        """
        comment_to_delete = TestCommentDelete.comment
        response = self.authorized_comment_author.delete(path=TestCommentDelete.url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(
            Comment.objects.filter(pk=comment_to_delete.pk).exists()
        )

    def test_delete_comment_by_admin(self):
        """Test that an admin can delete other users' comments.

        """
        comment_to_delete = TestCommentDelete.comment
        response = self.authorized_admin.delete(path=TestCommentDelete.url)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(
            Comment.objects.filter(pk=comment_to_delete.pk).exists()
        )
