from http import HTTPStatus

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from posts.models import Comment
from tests.factories import PostFactory, UserFactory, CommentFactory


class TestCommentUpdate(TestCase):
    """CommentUpdateView test suite"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = PostFactory()
        cls.comment = CommentFactory(post=cls.post)
        cls.user = cls.comment.author
        cls.another_user = UserFactory(username="another_user")
        cls.admin = UserFactory(is_staff=True)
        cls.url = f"/comments/{cls.comment.pk}/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_comment_author = APIClient()
        self.authorized_comment_author.force_login(TestCommentUpdate.user)

        self.authorized_another_user = APIClient()
        self.authorized_another_user.force_login(TestCommentUpdate.another_user)

        self.authorized_admin = APIClient()
        self.authorized_admin.force_login(TestCommentUpdate.admin)

    def test_update_comment_by_authorised_author(self):
        """Updating a comment by an authorised post author with valid data."""
        comment = TestCommentUpdate.comment
        start_time = timezone.now()
        data = {
            "text": "Тестовый коммент",
        }
        response = self.authorized_comment_author.patch(
            path=TestCommentUpdate.url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Comment.objects.filter(
                pk=comment.pk,
                post=TestCommentUpdate.post,
                text=data["text"],
                author=TestCommentUpdate.user,
                created=comment.created,
                updated__range=(start_time, timezone.now())
            ).exists()
        )

    def test_update_comment_by_admin(self):
        """Test that an admin user can edit other users' comments."""
        comment = TestCommentUpdate.comment
        start_time = timezone.now()
        data = {
            "text": "Тестовый коммент2",
        }
        response = self.authorized_admin.patch(
            path=TestCommentUpdate.url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Comment.objects.filter(
                pk=comment.pk,
                post=TestCommentUpdate.post,
                text=data["text"],
                author=TestCommentUpdate.user,
                created=comment.created,
                updated__range=(start_time, timezone.now()),
            ).exists()
        )

    def test_update_post_read_only_fields_cannot_be_edited(self):
        """Test that post, author, created and updated fields
        of the Comment model cannot be edited.

        """
        comment = TestCommentUpdate.comment
        another_post = PostFactory(title="another_post")
        data = {
            "post": another_post.pk,
            "author": TestCommentUpdate.another_user.pk,
            "created": "2023-01-01",
            "updated": "2023-01-01",
        }
        response = self.authorized_admin.patch(
            path=TestCommentUpdate.url,
            data=data,
            format='json',
        )
        updated_comment = Comment.objects.get(pk=comment.pk)
        post_data = (
            (comment.post, updated_comment.post),
            (comment.created, updated_comment.created),
            (comment.author, updated_comment.author)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(updated_comment.updated, data["updated"])
        for comment, updated_comment in post_data:
            with self.subTest(comment=comment, updated_comment=updated_comment):
                self.assertEqual(comment, updated_comment)

    def test_update_comment_by_not_author(self):
        """Test that an authorised user cannot edit other users' comments."""
        comment_to_update = TestCommentUpdate.comment
        data = {
            "text": "Измененный тестовый коммент",
            "author": TestCommentUpdate.another_user.pk,
            "post": PostFactory(title="some_post").pk,
        }
        response = self.authorized_another_user.patch(
            path=TestCommentUpdate.url,
            data=data,
            format='json',
        )
        comment_attempted_update = Comment.objects.get(pk=comment_to_update.pk)
        data_to_check = (
            (comment_to_update.text, comment_attempted_update.text),
            (comment_to_update.author, comment_attempted_update.author),
            (comment_to_update.post, comment_attempted_update.post),
            (comment_to_update.created, comment_attempted_update.created),
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        for comment, updated_comment in data_to_check:
            with self.subTest(comment=comment, updated_comment=updated_comment):
                self.assertEqual(comment, updated_comment)

    def test_update_comment_by_unauthorised_user(self):
        """Test that an unauthorised user cannot edit any comments."""
        comment_to_update = TestCommentUpdate.comment
        data = {
            "text": "Измененный тестовый коммент",
            "author": TestCommentUpdate.another_user.pk,
            "post": PostFactory(title="some_post").pk,
        }
        response = self.guest_client.patch(
            path=TestCommentUpdate.url,
            data=data,
            format='json',
        )
        comment_attempted_update = Comment.objects.get(pk=comment_to_update.pk)
        data_to_check = (
            (comment_to_update.text, comment_attempted_update.text),
            (comment_to_update.author, comment_attempted_update.author),
            (comment_to_update.post, comment_attempted_update.post),
            (comment_to_update.created, comment_attempted_update.created),
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        for comment, updated_comment in data_to_check:
            with self.subTest(comment=comment, updated_comment=updated_comment):
                self.assertEqual(comment, updated_comment)
