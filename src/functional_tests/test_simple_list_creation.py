from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 5


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_todo_list(self):
        # User has heard about a cooool new online to-do app.
        # and decicde to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He types "buy apples" into a text box
        inputbox.send_keys("buy apples")

        # When he hits enter. the page updates and now the page lists
        # "1: buy apples" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy apples")

        # There is still a text box invitig him to add another item.
        # He enters "buy watermelons"
        inputbox = self.get_item_input_box()
        inputbox.send_keys("buy watermelons")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on him list
        self.wait_for_row_in_list_table("1: buy apples")
        self.wait_for_row_in_list_table("2: buy watermelons")
        # Satisfied, he goes back to lifting

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("buy apples")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy apples")

        # She noticed that her list has a unique URL
        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site.

        ## We delete all the browser's cookies

        ## as a way of simulating a brand new user session
        self.browser.delete_all_cookies()

        # Francis visits the home page. There is not sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("buy apples", page_text)
        self.assertNotIn("buy watermelons", page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets hi own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
