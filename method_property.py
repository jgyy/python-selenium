"""
Selenium Web Driver. Useful methods and properties
"""
import json
import time
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException


def handler(event, context):
    """
    This is the default aws lambda handler
    :param event: aws event
    :param context: aws context
    :return: json status code and body
    """
    print(event, context)
    with Sele(event) as sele:
        try:
            obj = {
                "get text": sele.steam_get_text(),
                "get value": sele.steam_get_value(),
                "wrapper method": sele.steam_wrapper_method(),
                "element presense": sele.steam_element_presense(),
                "dynamic xpath": sele.steam_dynamic_xpath()
            }
            obj = json.dumps(obj)
        except KeyboardInterrupt:
            obj = {"error": str(KeyboardInterrupt)}
            print(KeyboardInterrupt)

    return {
        "statusCode": 200,
        "body": obj,
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
        self.options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome('/opt/chromedriver', options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        return True

    def steam_get_text(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/search"
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            for num in list(range(1, 8)):
                self.driver.implicitly_wait(4)
                self.driver.find_element(
                    By.XPATH, "//a[contains(text(),'>')]"
                ).click()
                self.driver.implicitly_wait(4)
                page = self.driver.find_element(
                    By.XPATH,
                    "//div[@class='search_pagination_left'][contains(text(), '{}')]".format(
                        str(num*25)
                    )
                ).get_attribute("innerText")
                self.driver.implicitly_wait(2)
                open_tab = self.driver.find_element(
                    By.XPATH, "//div[@id='search_results']"
                ).get_attribute("innerText")
                print(open_tab, page)
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        return body

    def steam_get_value(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/"
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            types = self.driver.find_elements(
                By.XPATH, "//*[@type]"
            )
            for html_type in types:
                print(html_type.get_attribute("type"))
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        return body

    def steam_wrapper_method(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/"
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            self.driver.implicitly_wait(1)
            types = self.driver.find_elements(By.XPATH, "//*[@type]")
            for html_type in types:
                print(html_type.get_attribute("type"))
            self.driver.implicitly_wait(1)
            ids = self.driver.find_elements(By.XPATH, "//*[@id]")
            for html_id in ids:
                print(html_id.get_attribute("id"))
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        return body

    def steam_element_presense(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/"
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            for one_char in string.ascii_lowercase:
                self.driver.implicitly_wait(1)
                text = self.driver.find_elements(
                    By.XPATH, "//*[contains(text(), '{}')]".format(one_char))
                for html_text in text:
                    print(html_text.get_attribute("innerText"))
        except NoSuchElementException:
            print("No more element presense.")
            self.driver.quit()
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        return body

    def steam_dynamic_xpath(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/search"
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            for one_char in string.ascii_lowercase:
                self.driver.implicitly_wait(1)
                search = self.driver.find_element(By.XPATH, "//input[@id='store_nav_search_term']")
                search.clear()
                search.send_keys(one_char)
                self.driver.implicitly_wait(1)
                self.driver.find_element(By.XPATH, "//a[contains(text(),'2')]").click()
                self.driver.implicitly_wait(1)
                result = self.driver.find_element(
                    By.XPATH, "//div[@id='search_results']").get_attribute("innerText")
                print(result)
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        return body


if __name__ == '__main__':
    START = time.time()
    HAND = handler('main', 'main')
    END = time.time()
    print("Time spent operating this lambda function: " + str(END - START) + " seconds")
