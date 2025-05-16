import os
import time
from datetime import datetime
from pathlib import Path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from collections.abc import Callable
from .container_commands import reset_database
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5

SCREEN_DUMP_LOCATION = Path(__file__).absolute().parent / "screendumps"

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.test_server = os.environ.get("TEST_SERVER")
        if self.test_server:
            self.live_server_url = "http://" + self.test_server
            reset_database(self.test_server)

    def tearDown(self) -> None:
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir(parents=True)
            self.take_screenshot()
            self.dump_html()
        self.browser.quit()
        super().tearDown()


    def _test_has_failed(self) -> bool:
        return self._outcome.result.failures or self._outcome.result.errors
    

    def take_screenshot(self) -> None:
        path = SCREEN_DUMP_LOCATION / self._get_filename("png")
        print("screenshotting to", path)
        self.browser.get_screenshot_as_file(str(path))


    def dump_html(self) -> None:
        path = SCREEN_DUMP_LOCATION / self._get_filename("html")
        print("dumping page HTML to", path)
        path.write_text(self.browser.page_source)


    def _get_filename(self, extension) -> None:
        timestamp = datetime.now().isoformat().replace(":", ".")[:19]
        return (
            f"{self.__class__.__name__}.{self._testMethodName}-{timestamp}.{extension}"
        )


    def wait(fn: Callable) -> Callable:
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)

        return modified_fn

    
    @wait
    def wait_for(self, fn: Callable) -> Callable:
        return fn()


    def get_item_input_box(self) -> WebElement:
        return self.browser.find_element(By.ID, "id_text")

    
    #Still don't know why exactly this one doesnt working with CSS_SELECTOR, just use By.ID 
    @wait
    def wait_to_be_logged_in(self, email: str) -> None:
        self.browser.find_element(By.ID, "id_logout")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)


    @wait
    def wait_to_be_logged_out(self, email: str) -> None:
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)

    
    @wait
    def wait_for_row_in_list_table(self, row_text: str) -> None:
        rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        self.assertIn(row_text, [row.text for row in rows])


    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr"))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")
    
