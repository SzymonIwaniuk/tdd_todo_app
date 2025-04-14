from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    


    def tearDown(self):
        self.browser.quit()
        

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])
                    

    def test_can_start_a_todo_list(self):
# User has heard about a cooool new online to-do app.
# and decicde to check out its homepage
        self.browser.get(self.live_server_url)

# He notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

# He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

# He types "buy apples" into a text box
        inputbox.send_keys("buy apples")

# When he hits enter. the page updates and now the page lists
# "1: buy apples" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        self.check_for_row_in_list_table("1: buy apples")

# There is still a text box invitig him to add another item.
# He enters "buy watermelons"
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("buy watermelons")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

# The page updates again, and now shows both items on him list
        self.check_for_row_in_list_table("1: buy apples")
        self.check_for_row_in_list_table("2: buy watermelons")

# Satisfied, he goes back to lifting


