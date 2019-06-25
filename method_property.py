"""
Selenium Web Driver. Useful methods and properties
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def handler(event, context):
    """
    :param event: aws event
    :param context: aws context
    :return: json status code and body
    """
    print(event, context)
    with Sele(event) as sele:
        try:
            obj = {
                "get text": sele.steam_get_text()
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
        base_url = "https://store.steampowered.com/"
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            for _ in list(range(0, 10)):
                self.driver.find_element(
                    By.XPATH, "//div[@id='home_maincap_v7']//div[@class='arrow right']"
                ).click()
                self.driver.implicitly_wait(1)
                open_tab = self.driver.find_element(
                    By.XPATH, "//div[@class='home_cluster_ctn home_ctn']"
                ).get_attribute("innerText")
                self.driver.implicitly_wait(1)
                print(open_tab)

            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body


if __name__ == '__main__':
    START = time.time()
    HAND = handler('main', 'main')
    END = time.time()
    print("Time spent operating this lambda function: " + str(END - START) + " seconds")