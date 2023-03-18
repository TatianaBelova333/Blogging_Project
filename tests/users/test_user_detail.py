from http import HTTPStatus

from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from tests.factories import UserFactory
from users.serializers import UserDetailSerializer


class TestUserDetail(TestCase):
    """Test suite for retrieving a single user by pk."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.url = f"/users/{cls.user.pk}/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestUserDetail.user)

    def test_user_detail_by_authorised_user(self):
        """Test for retrieving a single user by an authorised user."""
        user = TestUserDetail.user
        response = self.authorized_client.get(path=TestUserDetail.url)
        expected_response_data = UserDetailSerializer(user).data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_response_data)

    def test_user_detail_by_unauthorised_user(self):
        """Test for retrieving a single user by an unauthorised user."""
        response = self.guest_client.get(path=TestUserDetail.url)
        expected_response_data = {
            'detail': ErrorDetail(
                string='Authentication credentials were not provided.',
                code='not_authenticated'
            )
        }
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, expected_response_data)
