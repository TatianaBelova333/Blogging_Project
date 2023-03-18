from http import HTTPStatus

from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from tests.factories import UserFactory
from users.models import User


class TestUserUpdate(TestCase):
    """Test suite for updating users."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.url = f"/users/{cls.user.pk}/"

    def setUp(self):
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        self.authorized_client.force_login(TestUserUpdate.user)

        self.another_authorised_user = APIClient()
        self.another_authorised_user.force_login(UserFactory(username='another_user'))

        self.admin_user = APIClient()
        self.admin_user.force_login(UserFactory(is_staff=True))

    def test_update_user_authorised(self):
        """Updating user with valid data by an authorised user."""
        user = TestUserUpdate.user
        data = {
            "username": "belka",
            "birthday": "1987-12-01",
            "phone_number": "+79092345676",
            "password": "kjfr1234g",
            "email": "belka@yandex.ru",
        }

        response = self.authorized_client.put(
            path=TestUserUpdate.url,
            data=data,
            format='json',
        )
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            User.objects.filter(
                id=user.pk,
                username=data["username"],
                birthday=data["birthday"],
                phone_number=data["phone_number"],
                email=data["email"],
            ).exists()
        )
        self.assertTrue(check_password(data["password"], updated_user.password))

    def test_update_user_weak_password(self):
        """Updating user with valid data by an authorised user."""
        data = {
            "password": "kjfr1",
        }

        response = self.authorized_client.patch(
            path=TestUserUpdate.url,
            data=data,
            format='json',
        )
        expected_response_data = {
            'password': [ErrorDetail(
                string='Пароль должен содержать не менее 8 символов,из которых хотя бы одна цифра.',
                code='password_is_weak'
            )]
        }
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)

    def test_update_user_wrong_email_domain(self):
        """Updating user with valid data by an authorised user."""
        data = {
            "email": "user@gmail.com",
        }

        response = self.authorized_client.patch(
            path=TestUserUpdate.url,
            data=data,
            format='json',
        )
        expected_response_data = {
            'email': [ErrorDetail(
                string='Разрешены только: mail.ru; yandex.ru',
                code='invalid')]
        }
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)

    def test_update_user_unauthorised(self):
        """Updating user with valid data by an unauthorised user."""
        user_to_update = TestUserUpdate.user
        data = {
            "username": "misha",
            "birthday": "1987-12-01",
            "phone_number": "+79092345670",
            "password": "kjfrhU782",
            "email": "misha@yandex.ru",
        }

        response = self.guest_client.put(
            path=TestUserUpdate.url,
            data=data,
            format='json',
        )
        user_attempted_update = User.objects.get(pk=user_to_update.pk)
        data = (
            (user_to_update.username, user_attempted_update.username),
            (user_to_update.birthday, user_attempted_update.birthday),
            (user_to_update.phone_number, user_attempted_update.phone_number),
            (user_to_update.email, user_attempted_update.email),
        )

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        for user_to_update, user_attempted_update in data:
            with self.subTest(
                    user_to_update=user_to_update,
                    user_attempted_update=user_attempted_update,
            ):
                self.assertEqual(user_to_update, user_attempted_update)

    def test_update_user_by_another_user(self):
        """Updating user with valid data by another authorised user."""
        user_to_update = TestUserUpdate.user
        data = {
            "username": "grisha",
            "birthday": "1987-12-01",
            "phone_number": "+79092345670",
            "password": "kjfrhU782",
            "email": "grisha@yandex.ru",
        }
        response = self.another_authorised_user.put(
            path=TestUserUpdate.url,
            data=data,
            format='json',
        )
        user_attempted_update = User.objects.get(pk=user_to_update.pk)
        data = (
            (user_to_update.username, user_attempted_update.username),
            (user_to_update.birthday, user_attempted_update.birthday),
            (user_to_update.phone_number, user_attempted_update.phone_number),
            (user_to_update.email, user_attempted_update.email),
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        for user_to_update, user_attempted_update in data:
            with self.subTest(
                    user_to_update=user_to_update,
                    user_attempted_update=user_attempted_update,
            ):
                self.assertEqual(user_to_update, user_attempted_update)

    def test_update_user_by_admin(self):
        """Updating user with valid data by another user with admin rights."""
        user_to_update = TestUserUpdate.user
        data = {
            "username": "sparrow",
            "birthday": "1988-12-01",
            "phone_number": "+79092345619",
            "password": "kjfrhU782",
            "email": "sparrow@yandex.ru",
        }
        response = self.admin_user.put(
            path=TestUserUpdate.url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            User.objects.filter(
                pk=user_to_update.pk,
                username=data["username"],
                birthday=data["birthday"],
                phone_number=data["phone_number"],
                email=data["email"],
            ).exists()
        )
