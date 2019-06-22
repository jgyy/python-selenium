"""
Simple Usage with headless chrome
layers are located at /opt/ directory.
"""
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException


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
        except NoSuchElementException:
            raise NoSuchElementException
        except ElementNotVisibleException:
            raise ElementNotVisibleException
        except WebDriverException:
            raise WebDriverException
        finally:
            driver.quit()
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
        except NoSuchElementException:
            raise NoSuchElementException
        except ElementNotVisibleException:
            raise ElementNotVisibleException
        except WebDriverException:
            raise WebDriverException
        finally:
            driver.quit()
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
        except NoSuchElementException:
            raise NoSuchElementException
        except ElementNotVisibleException:
            raise ElementNotVisibleException
        except WebDriverException:
            raise WebDriverException
        finally:
            driver.quit()
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
        except NoSuchElementException:
            raise NoSuchElementException
        except ElementNotVisibleException:
            raise ElementNotVisibleException
        except WebDriverException:
            raise WebDriverException
        finally:
            driver.quit()
        return body

    def element_govtech_by_class(self):
        """
        :return: search result from govtech website
        """
        driver = self.browser('main')
        base_url = "https://www.tech.gov.sg/media/"
        driver.get(base_url)
        try:
            # noinspection PyArgumentEqualDefault
            driver.find_element(By.ID, "2008")
            print("We found an element by id='2008'")
            driver.find_element(By.XPATH, "//input[@id='search-box']")
            print("We found an element by xpath='//input[@id='search-box']'")
            driver.find_element(By.LINK_TEXT, "Overview")
            print("We found an element by link_text='Overview'")
            body = driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            raise NoSuchElementException
        except ElementNotVisibleException:
            raise ElementNotVisibleException
        except WebDriverException:
            raise WebDriverException
        finally:
            driver.quit()
        return body

    def govtech_list_of_elements(self):
        """
        :return: search result from govtech website
        """
        driver = self.browser('main')
        base_url = "https://www.tech.gov.sg/contact-us/"
        driver.get(base_url)
        try:
            class_list = driver.find_elements_by_class_name("row")
            print("ClassName -> Size of the list is: " + str(len(class_list)))
            tag_list = driver.find_elements_by_tag_name("div")
            print("TagName -> Size of the list is: " + str(len(tag_list)))
            body = driver.find_element_by_xpath("//div[@id='main-content']").text
            print(body)
        except NoSuchElementException:
            raise NoSuchElementException
        except ElementNotVisibleException:
            raise ElementNotVisibleException
        except WebDriverException:
            raise WebDriverException
        finally:
            driver.quit()
        return body


if __name__ == '__main__':
    HAND = handler('main', 'main')
