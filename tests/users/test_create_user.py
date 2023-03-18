from http import HTTPStatus
import random

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from users.models import User

ALLOWED_DOMAINS = settings.ALLOWED_EMAIL_DOMAINS
URL = "/users/"


class TestUserCreate(TestCase):
    """UserCreateView test suite"""

    def setUp(self):
        self.guest_client = APIClient()

    def test_create_user_success(self):
        """User registration with valid data."""
        data = {
            "username": "belka",
            "birthday": "1987-12-01",
            "phone_number": "+79092345676",
            "password": "kjfrhU782",
        }

        response = self.guest_client.post(
            path=URL,
            data=data,
            format='json',
        )
        added_user = User.objects.filter(
                username=data['username'],
                birthday=data["birthday"],
                phone_number=data["phone_number"],
            )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(added_user.exists())
        self.assertNotEqual(added_user.first().password, data["password"])

    def test_create_user_weak_password(self):
        """User registration with a weak password"""

        user_data = {
            "short_password": {
                "username": "misha",
                "birthday": "1987-12-01",
                "phone_number": "+79092345670",
                "password": "kjfr4h",
            },
            "password_no_digit": {
                "username": "alena",
                "birthday": "1988-12-01",
                "phone_number": "+79092345680",
                "password": "kjfrhsdkdkkdd",
            }
        }
        expected_response_data = {
            'password': [ErrorDetail(
                string='Пароль должен содержать не менее 8 символов,из которых хотя бы одна цифра.',
                code='password_is_weak'
            )]
        }
        for data in user_data.values():
            with self.subTest(data=data):
                response = self.guest_client.post(
                    path=URL,
                    data=data,
                    format='json',
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
                self.assertEqual(response.data, expected_response_data)
                self.assertFalse(
                    User.objects.filter(
                        username=data['username'],
                        birthday=data['birthday'],
                        phone_number=data['phone_number'],
                    ).exists())

    def test_create_user_wrong_email_domain(self):
        """User registration with forbidden email domains."""

        data = {
            "username": "new_user",
            "birthday": "2000-12-01",
            "phone_number": "+79092345698",
            "email": "user@gmail.com",
            "password": "kjfrhU782",
        }

        response = self.guest_client.post(
            path=URL,
            data=data,
            format='json',
        )
        expected_response_data = {
            "email": [ErrorDetail(
                string=f"Разрешены только: {'; '.join(ALLOWED_DOMAINS)}",
                code='invalid')]
        }
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)
        self.assertFalse(
            User.objects.filter(
                username=data["username"],
                birthday=data["birthday"],
                phone_number=data["phone_number"],
                email=data["email"],
            ).exists()
        )

    def test_create_user_allowed_email_domain(self):
        """User registration with allowed email domains."""
        random_domain = random.choice(ALLOWED_DOMAINS)

        data = {
            "username": "another_user",
            "birthday": "2000-12-01",
            "phone_number": "+79092345680",
            "email": "user@" + random_domain,
            "password": "kjfrhU782",
        }

        response = self.guest_client.post(
            path=URL,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(
            User.objects.filter(
                username=data['username'],
                birthday=data["birthday"],
                phone_number=data["phone_number"],
                email=data["email"],
            ).exists()
        )
