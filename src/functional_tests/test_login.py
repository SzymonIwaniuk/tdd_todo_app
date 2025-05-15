import re

from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

TEST_EMAIL = "user@example.com"
SUBJECT = "Your login link for Superlists"


class Login(FunctionalTest):
    def test_login_using_magic_link(self) -> None:
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(
            TEST_EMAIL, Keys.ENTER
        )

        self.wait_for(
            lambda: self.assertIn(
                "Check your email",
                self.browser.find_element(By.CSS_SELECTOR, "body").text,
            )
        )

        email = mail.outbox.pop()
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        self.assertIn("Use this link to log in", email.body)

        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        self.browser.get(url)
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout"),
        )

        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)


        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout"),
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)


        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()

        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(TEST_EMAIL, navbar.text)


        # user is logged in
        #self.wait_to_be_logged_in(email=TEST_EMAIL)


        # now he logs out
        #self.browser.find_element(By.CSS_SELECTOR, '#id_logout').click()
        

        # he is logged out
        #self.wait_to_be_logged_out(email=TEST_EMAIL)
