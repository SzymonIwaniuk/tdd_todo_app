from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
# User has heard about a cooool new online to-do app.
# and decicde to check out its homepage
        self.browser.get("http://localhost:8000")

# He notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)


# He is invited to enter a to-do item straight away
        self.fail("Finish the test!")
# He types "cwiara w martwym byqu" into a text box

# When he hits enter. the page updates and now the page lists
# "1: cwiara w martwym byqu" as an item in a to-do list

# There is still a text box invitig him to add another item.
# He enters "4 x champion powerlifter"

# The page updates again, and now shows both items on him list

# Satisfied, he goes back to lifting

if __name__ == '__main__':
    unittest.main()

