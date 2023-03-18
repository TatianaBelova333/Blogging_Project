from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from tests.factories import UserFactory
from users.models import User

ALLOWED_DOMAINS = settings.ALLOWED_EMAIL_DOMAINS


class TestUserList(TestCase):
    """Test suite for retrieving a list of users."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        UserFactory.create_batch(size=10)
        cls.user = UserFactory()
        cls.url = "/users/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestUserList.user)

    def test_user_list_authorised(self):
        """Test for retrieving a list of users by an authorised user."""
        response = self.authorized_client.get(path=TestUserList.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), User.objects.count())

    def test_user_list_unauthorised(self):
        """Test for retrieving a list of users by an unauthorised user."""
        response = self.guest_client.get(path=TestUserList.url)
        expected_response_data = {
            'detail': ErrorDetail(
                string='Authentication credentials were not provided.',
                code='not_authenticated'
            )
        }
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, expected_response_data)
