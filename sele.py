"""
Simple Usage with headless chrome
layers are located at /opt/ directory.
"""
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


def handler(event, context):
    """
    blue development server ip: 13.250.110.171
    :param event: aws event
    :param context: aws context
    :return: json status code and body
    """
    print(event, context)
    sele = Sele()
    try:
        obj = {
            "id name": sele.element_govtech_id_name(),
            "xpath css": sele.element_govtech_xpath_css(),
            "link text": sele.element_govtech_link_text(),
            "class tag": sele.element_govtech_class_tag()
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
    Initiate the driver instance
    """
    options = Options()

    def browser(self, event):
        """
        :param event: only used to set headless chrome option
        :return: web driver configuration
        """
        if event != 'main':
            self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome('/opt/chromedriver', options=self.options)

    def element_govtech_id_name(self):
        """
        :return: search result from govtech website
        """
        driver = self.browser('main')
        base_url = "https://www.tech.gov.sg"
        driver.get(base_url)
        try:
            driver.find_element_by_id("navbar")
            print("We found an element by id='navbar'")
            driver.find_element_by_name("viewport")
            print("We found an element by name='viewport'")
            body = driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
            driver.quit()
        except NoSuchElementException:
            body = NoSuchElementException
        except ElementNotVisibleException:
            body = ElementNotVisibleException
        return body

    def element_govtech_xpath_css(self):
        """
        :return: search result from govtech website
        """
        driver = self.browser('main')
        base_url = "https://www.tech.gov.sg/digital-government-transformation/"
        driver.get(base_url)
        try:
            driver.find_element_by_xpath("//input[@id='search-box-mobile']")
            print("We found an element by xpath='//input[@id='search-box-mobile']'")
            driver.find_element_by_css_selector("#search-activate")
            print("We found an element by css='#search-activate'")
            body = driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
            driver.quit()
        except NoSuchElementException:
            body = NoSuchElementException
        except ElementNotVisibleException:
            body = ElementNotVisibleException
        return body

    def element_govtech_link_text(self):
        """
        :return: search result from govtech website
        """
        driver = self.browser('main')
        base_url = "https://www.tech.gov.sg/who-we-are/our-role/"
        driver.get(base_url)
        try:
            driver.find_element_by_link_text("A Singapore Government Agency Website")
            print("We found an element by link_text='A Singapore Government Agency Website'")
            driver.find_element_by_partial_link_text("Digital")
            print("We found an element by partial_link_text='Digital'")
            body = driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
            driver.quit()
        except NoSuchElementException:
            body = NoSuchElementException
        except ElementNotVisibleException:
            body = ElementNotVisibleException
        return body

    def element_govtech_class_tag(self):
        """
        :return: search result from govtech website
        """
        driver = self.browser('main')
        base_url = "https://www.tech.gov.sg/careers/overview/"
        driver.get(base_url)
        try:
            driver.find_element_by_class_name("navbar-burger").click()
            key = driver.find_element_by_class_name("input")
            key.send_keys("test")
            print("We found an element by class_name='input'")
            key_text = driver.find_element_by_tag_name("div")
            print("We found an element by tag_name=" + key_text.text)
            body = driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
            driver.quit()
        except NoSuchElementException:
            body = NoSuchElementException
        except ElementNotVisibleException:
            body = ElementNotVisibleException
        return body


if __name__ == '__main__':
    HAND = handler('main', 'main')
