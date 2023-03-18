from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from posts.serializers import CommentDetailSerializer
from tests.factories import UserFactory, CommentFactory


class TestCommentDetail(TestCase):
    """Test suite for retrieving a single comment."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.comment = CommentFactory()
        cls.url = f"/comments/{cls.comment.pk}/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestCommentDetail.user)

    def test_comment_detail_authorised_user(self):
        """Test for retrieving a single comment by an authorised user."""
        comment = TestCommentDetail.comment
        response = self.authorized_client.get(path=TestCommentDetail.url)
        expected_response_data = CommentDetailSerializer(comment).data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_response_data)

    def test_comment_detail_unauthorised_user(self):
        """Test for retrieving a single comment by an unauthorised user."""
        comment = TestCommentDetail.comment
        response = self.authorized_client.get(path=TestCommentDetail.url)
        expected_response_data = CommentDetailSerializer(comment).data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_response_data)
