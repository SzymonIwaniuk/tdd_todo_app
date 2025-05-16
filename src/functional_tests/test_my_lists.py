from django.conf import settings
from .base import FunctionalTest
from .container_commands import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from selenium.webdriver.common.by import By


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email: str) -> None:
        if self.test_server:
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path="/",
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self) -> None:
        self.create_pre_authenticated_session("user@example.com")
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        self.wait_for(
            lambda: self.assertIn(
                "user@example.com",
                self.browser.find_element(By.CSS_SELECTOR, "h2").text,
            )
        )

        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines")
        )

        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Click cows"))
        self.browser.find_element(By.LINK_TEXT, "Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(By.LINK_TEXT, "My lists"),
                [],
            )
        )
