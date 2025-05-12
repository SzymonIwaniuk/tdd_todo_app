from django.test import TestCase
from unittest import mock

class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self) -> None:
        response = self.client.post(
            "/accounts/send_login_email", data={"email": "user@example.com"}
        )
        self.assertRedirects(response, "/")

    @mock.patch("accounts.views.send_mail")
    def test_send_mail_to_address_from_post(self, mock_send_mail) -> None:

        self.client.post(
            "/accounts/send_login_email", data={"email": "user@example.com"}
        )

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(to_list, ["user@example.com"])


