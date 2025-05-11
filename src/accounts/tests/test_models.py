from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self) -> None:
        user = User(email="a@b.com")
        user.full_clean()

    def test_email_is_primary_key(self) -> None:
        user = User(email="a@b.com")
        self.assertEqual(user.pk, "a@b.com")

