from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Comment
from posts.serializers import PostDetailSerializer
from tests.factories import UserFactory, PostFactory, CommentFactory


class TestPostDetail(TestCase):
    """Test suite for retrieving a single post."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.post = PostFactory()
        cls.url = f"/posts/{cls.post.pk}/"
        CommentFactory.create_batch(size=5, post=cls.post)
        CommentFactory.create_batch(size=5, post=PostFactory(title='another_post'))

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestPostDetail.user)

    def test_post_detail_authorised_user(self):
        """Test for retrieving a single post by an authorised user."""
        post = TestPostDetail.post
        response = self.authorized_client.get(path=TestPostDetail.url)
        expected_response_data = PostDetailSerializer(post).data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_response_data)

    def test_post_detail_unauthorised_user(self):
        """Test for retrieving a single post by an unauthorised user."""
        post = TestPostDetail.post
        response = self.guest_client.get(path=TestPostDetail.url)
        expected_response_data = PostDetailSerializer(post).data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_response_data)

    def test_post_has_correct_comments(self):
        """Test that the post has only the comments related to the post."""
        post = TestPostDetail.post
        response = self.guest_client.get(path=TestPostDetail.url)
        post_comments = Comment.objects.filter(post=post.pk).values_list('pk', flat=True)
        self.assertQuerysetEqual(response.data["comments"], post_comments)
