from django.test import TestCase
from accounts.models import Token
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

    @mock.patch("accounts.views.messages")
    def test_adds_succes_message(self, mock_messages) -> None:
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "user@example.com"},
        )

        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(
            mock_messages.success.call_args,
            mock.call(response.wsgi_request, expected),
        )


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self) -> None:
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")


    def test_creates_token_associated_with_email(self) -> None:
        self.client.post(
            "/accounts/send_login_email", data={"email": "user@example.com"}
        )
        token = Token.objects.get()
        self.assertEqual(token.email, "user@example.com")


    @mock.patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail) -> None:
        self.client.post(
            "/accounts/send_login_email", data={"email": "user@example.com"}
        )

        token = Token.objects.get()
        expected_url = f"https://testserver/accounts/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
