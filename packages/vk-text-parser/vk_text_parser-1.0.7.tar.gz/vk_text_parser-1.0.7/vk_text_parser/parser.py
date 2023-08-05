import os
import time
import sys

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options

from .models import ParsedElement


class VkTxtParser(object):
    step = 5
    max_offset = 20
    timeout = 2
    content_xpath = '''//div[@id='public_wall']//*[@class='wall_text'][count(div)=1]/div[count(div)=1]'''
    ignore_text = 'Показать полностью'

    def __init__(self, public):
        self.public = public
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        if sys.platform in ('linux', 'linux2'):
            driver_dir = 'linux'
        elif sys.platform == "darwin":
            driver_dir = 'mac'
        else:
            raise RuntimeError("Unsupported platform")
        driver_location = os.path.join(os.path.dirname(__file__), 'drivers', driver_dir, 'chromedriver')
        self.driver = webdriver.Chrome(executable_path=os.path.abspath(driver_location), chrome_options=chrome_options)

    def __del__(self):
        driver = getattr(self, 'driver', None)
        if driver:
            driver.close()

    def get_full_html(self, public):
        self.driver.get('http://vk.com/%s' % public)
        wait = ui.WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element_by_id('page_avatar'))
        push_counter = 0
        while push_counter < self.max_offset:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            push_counter += 1
            time.sleep(0.5)

    def parse(self):
        public = self.public
        assert public is not NotImplemented
        self.get_full_html(public)
        wall_divs = self.driver.find_elements_by_xpath(self.content_xpath)
        wall_divs.reverse()
        return filter(lambda t: self.ignore_text.lower() not in t.text.lower(),
                      map(lambda w: ParsedElement(w.get_attribute('id'), w.text), wall_divs))
