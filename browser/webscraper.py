from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import itertools
import datetime


'''
remote_address='host.docker.internal:4444/wd/hub'
'''
class Browser:
    def __init__(self, headless=False, delay=2
                , remote_address='host.docker.internal:4444/wd/hub'):
        self.driver = None
        self.wait = None
        self.remote_address = remote_address
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--window-size=2560x1440")

        if headless:
            self.chrome_options.add_argument("headless")
        self.start_browser()

    def browser(self):
        return webdriver.Remote(
                       command_executor=self.remote_address
                     , desired_capabilities=DesiredCapabilities.CHROME
                     , options=self.chrome_options)

    def start_browser(self, delay=2):
        self.driver = self.browser()
        self.change_delay(delay)

    def restart_browser(self, delay=2):
        self.shutdown()
        self.start_browser(delay)

    def change_delay(self, delay):
        self.wait = WebDriverWait(self.driver, delay)

    def wait_xpath(self, xpath):
        element = self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        return element

    def take_screenshots(self, name='screenshots'):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H%M%S")
        # Create folder
        import os
        os.makedirs('Screenshots', exist_ok=True)

        screenshot_name = 'Screenshots//{0}_{1}.png'.format(name, date)
        self.driver.get_screenshot_as_file(screenshot_name)

    def load_page(self, address):
        self.driver.get(address)

    def get_soup(self):
        return BeautifulSoup(self.driver.page_source, "lxml")

    def scroll_down(self, nr=5):
        for sec in range(nr):
            self.driver.execute_script("window.scrollTo(0, 10000)")
            time.sleep(1)

    def scroll_down_simple(self, nr=5):
        for sec in range(nr):
            self.driver.execute_script("window.scrollTo(0, 10000)")
            time.sleep(1)

    # @try_dec
    def get_text_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath).text

    # @try_dec
    def get_url(self):
        return self.driver.current_url

    # @try_dec
    def fill_box(self, box, query):
        box = xpath_soup(box)
        box = self.wait_xpath(box)
        box.clear()
        box.send_keys(query)

    # @try_dec
    def click(self, btn):
        button = xpath_soup(btn)
        button = self.wait_xpath(button)
        button.click()

    # @try_dec
    def wait_till_loaded(self, xpath):
        self.wait_xpath(xpath)

    # @try_dec
    def key_down(self, key):
        key = xpath_soup(key)
        button = self.wait_xpath(key)
        button.send_keys(Keys.ARROW_DOWN)

    # @try_dec
    def key_enter(self, key):
        key = xpath_soup(key)
        button = self.wait_xpath(key)
        button.send_keys(Keys.RETURN)

    def shutdown(self):
        self.driver.quit()


# https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def try_dec(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            error_log = "Error in function: {0} with args:{1} \n{2}".format(func.__name__, args[1], ex)
            # log
            try:
                with open("log.txt", "a") as my_file:
                    # add self.driver.current_url
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                    my_file.write("{0} {1}\n".format(now, error_log))
            except PermissionError:
                print(error_log)
            return 0

    return wrapper