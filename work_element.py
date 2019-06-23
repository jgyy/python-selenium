"""
Simple Usage with headless chrome
AWS lambda layers are located at /opt/ directory.
Note that env will never be commited remotely
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from env import (EMAIL, PASSWORD)


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
                "browser interation": sele.fortnite_browser_interactions(),
                "click send": sele.fortnite_click_keys()
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
        return True

    def fortnite_browser_interactions(self):
        """
        :return: search result from fortnite website
        """
        base_url = "https://www.epicgames.com/fortnite/en-US/battle-pass/season-9"
        self.driver.maximize_window()
        self.driver.get(base_url)
        try:
            title = self.driver.title
            print("Title of the webpage is: " + title)
            current_url = self.driver.current_url
            print("Current Url of the web page is: " + current_url)
            self.driver.refresh()
            print("Browser Refreshed 1st time")
            self.driver.get(self.driver.current_url)
            print("Browser Refreshed 2nd time")
            self.driver.get("https://www.epicgames.com/fortnite/en-US/play-now/battle-royale")
            current_url = self.driver.current_url
            print("Current Url of the web page is: " + current_url)
            self.driver.back()
            print("Go one step back in browser history")
            current_url = self.driver.current_url
            print("Current Url of the web page is: " + current_url)
            self.driver.forward()
            print("Go one step forward in browser history")
            current_url = self.driver.current_url
            print("Current Url of the web page is: " + current_url)

            body = self.driver.find_element(By.XPATH, "//div[contains(@id, 'ReactWrapper')]").text
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def fortnite_click_keys(self):
        """
        :return: search result from fortnite website
        """
        base_url = "https://www.epicgames.com/store/en-US/"
        self.driver.maximize_window()
        self.driver.get(base_url)
        try:
            self.driver.find_element(By.XPATH, "//a[contains(@title,'Sign In')]").click()
            self.driver.find_element(
                By.XPATH, "//input[@id='epic_username']"
            ).send_keys(EMAIL)
            self.driver.find_element(
                By.XPATH, "//input[@id='password']"
            ).send_keys(PASSWORD, Keys.RETURN)

            self.driver.implicitly_wait(2)
            body = self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'ReactWrapper')]").text
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
