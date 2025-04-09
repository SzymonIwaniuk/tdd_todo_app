from django.test import TestCase
from django.http import HttpRequest, response
from lists.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        #self.assertContains(response, "<title>To-Do lists</title>")
        #self.assertContains(response, "<html>")
        #self.assertContains(response, "</html>")
        
        #refactoring
        self.assertTemplateUsed(response, "home.html")
    
    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")


