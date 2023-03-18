from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Comment
from posts.serializers import CommentDetailSerializer
from tests.factories import UserFactory, CommentFactory, PostFactory


class TestCommentList(TestCase):
    """Test suite for retrieving a list of comments."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = PostFactory()
        CommentFactory.create_batch(size=10, post=cls.post)
        CommentFactory.create_batch(size=10, post=PostFactory(title="Another post"))
        cls.user = UserFactory()
        cls.url = "/comments/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestCommentList.user)

    def test_comment_list_authorised(self):
        """Test for retrieving a list of comments by an authorised user."""
        response = self.authorized_client.get(path=TestCommentList.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Comment.objects.count())

    def test_comment_list_unauthorised(self):
        """Test for retrieving a list of comments by an unauthorised user."""
        response = self.guest_client.get(path=TestCommentList.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Comment.objects.count())

    def test_comment_list_filter_by_post(self):
        """Test for retrieving a list of comments filtered by a post."""
        post = TestCommentList.post
        expected_result = CommentDetailSerializer(
            Comment.objects.filter(post=post.pk).all(),
            many=True,
        ).data

        path = TestCommentList.url + f'?post={post.pk}'
        response = self.guest_client.get(path=path)
        self.assertListEqual(response.data, expected_result)

