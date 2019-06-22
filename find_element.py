"""
Simple Usage with headless chrome
layers are located at /opt/ directory.
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotVisibleException, WebDriverException
)


def handler(event, context):
    """
    blue development server ip: 13.250.110.171
    :param event: aws event
    :param context: aws context
    :return: json status code and body
    """
    print(event, context)
    with Sele(event) as sele:
        try:
            obj = {
                "id name": sele.element_govtech_id_name(),
                "xpath css": sele.element_govtech_xpath_css(),
                "link text": sele.element_govtech_link_text(),
                "class tag": sele.element_govtech_class_tag(),
                "by class": sele.element_govtech_by_class(),
                "element list": sele.govtech_list_of_elements()
            }
        except KeyboardInterrupt:
            obj = {"error": KeyboardInterrupt}
            print(KeyboardInterrupt)

    return {
        "statusCode": 200,
        "body": json.dumps(obj),
        'headers': {'Content-Type': 'application/json'}
    }


class Sele:
    """
    Initiate the driver instance.
    Since this is a file system, you have to instantiate this class by writing...
    with Sele(event) as sele:
    """

    def __init__(self, event):
        self.event = event
        self.driver = None
        self.options = Options()

    def __enter__(self):
        if self.event != 'main':
            self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('/opt/chromedriver', options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        if exc_type or exc_val or exc_tb:
            return str(exc_type, exc_val, exc_tb)
        return True

    def element_govtech_id_name(self):
        """
        :return: search result from govtech website
        """
        base_url = "https://www.tech.gov.sg"
        self.driver.get(base_url)
        body = ""
        try:
            self.driver.find_element_by_id("navbar")
            print("We found an element by id='navbar'")
            self.driver.find_element_by_name("viewport")
            print("We found an element by name='viewport'")
            body = self.driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            print(NoSuchElementException)
        except ElementNotVisibleException:
            print(ElementNotVisibleException)
        except WebDriverException:
            print(WebDriverException)
        return body

    def element_govtech_xpath_css(self):
        """
        :return: search result from govtech website
        """
        base_url = "https://www.tech.gov.sg/digital-government-transformation/"
        self.driver.get(base_url)
        body = ""
        try:
            self.driver.find_element_by_xpath("//input[@id='search-box-mobile']")
            print("We found an element by xpath='//input[@id='search-box-mobile']'")
            self.driver.find_element_by_css_selector("#search-activate")
            print("We found an element by css='#search-activate'")
            body = self.driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            print(NoSuchElementException)
        except ElementNotVisibleException:
            print(ElementNotVisibleException)
        except WebDriverException:
            print(WebDriverException)
        return body

    def element_govtech_link_text(self):
        """
        :return: search result from govtech website
        """
        base_url = "https://www.tech.gov.sg/who-we-are/our-role/"
        self.driver.get(base_url)
        body = ""
        try:
            self.driver.find_element_by_link_text("A Singapore Government Agency Website")
            print("We found an element by link_text='A Singapore Government Agency Website'")
            self.driver.find_element_by_partial_link_text("Digital")
            print("We found an element by partial_link_text='Digital'")
            body = self.driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            print(NoSuchElementException)
        except ElementNotVisibleException:
            print(ElementNotVisibleException)
        except WebDriverException:
            print(WebDriverException)
        return body

    def element_govtech_class_tag(self):
        """
        :return: search result from govtech website
        """
        base_url = "https://www.tech.gov.sg/careers/overview/"
        self.driver.get(base_url)
        body = ""
        try:
            self.driver.find_element_by_class_name("navbar-burger").click()
            key = self.driver.find_element_by_class_name("input")
            key.send_keys("test")
            print("We found an element by class_name='input'")
            key_text = self.driver.find_element_by_tag_name("div")
            print("We found an element by tag_name=" + key_text.text)
            body = self.driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            print(NoSuchElementException)
        except ElementNotVisibleException:
            print(ElementNotVisibleException)
        except WebDriverException:
            print(WebDriverException)
        return body

    def element_govtech_by_class(self):
        """
        :return: search result from govtech website
        """
        base_url = "https://www.tech.gov.sg/media/"
        self.driver.get(base_url)
        body = ""
        try:
            # noinspection PyArgumentEqualDefault
            self.driver.find_element(By.ID, "2008")
            print("We found an element by id='2008'")
            self.driver.find_element(By.XPATH, "//input[@id='search-box']")
            print("We found an element by xpath='//input[@id='search-box']'")
            self.driver.find_element(By.LINK_TEXT, "Overview")
            print("We found an element by link_text='Overview'")
            body = self.driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            print(NoSuchElementException)
        except ElementNotVisibleException:
            print(ElementNotVisibleException)
        except WebDriverException:
            print(WebDriverException)
        return body

    def govtech_list_of_elements(self):
        """
        :return: search result from govtech website
        """
        base_url = "https://www.tech.gov.sg/contact-us/"
        self.driver.get(base_url)
        body = ""
        try:
            class_list = self.driver.find_elements_by_class_name("row")
            print("ClassName -> Size of the list is: " + str(len(class_list)))
            tag_list = self.driver.find_elements_by_tag_name("div")
            print("TagName -> Size of the list is: " + str(len(tag_list)))
            body = self.driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            print(NoSuchElementException)
        except ElementNotVisibleException:
            print(ElementNotVisibleException)
        except WebDriverException:
            print(WebDriverException)
        return body


if __name__ == '__main__':
    START = time.time()
    HAND = handler('main', 'main')
    END = time.time()
    print("Time spent opening 6 webpage and retrieve data: " + str(END - START) + " seconds")
