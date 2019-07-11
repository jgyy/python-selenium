"""
Selenium Web Driver. Useful methods and properties
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from env import U, P


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
                "implicit wait": sele.steam_implicit_wait(),
                "explicit wait": sele.expedia_explicit_wait(),
                "expedia work": sele.expedia_explicit_work()
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
    Initiate the driver instance and run the functions below.
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
        self.options.add_argument('--window-size=1600,900')
        self.driver = webdriver.Chrome('/opt/chromedriver', options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        return True

    def steam_implicit_wait(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/"
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, "//a[@class='global_action_link']").click()
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, "//input[@id='input_username']").send_keys(U)
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, "//input[@id='input_password']").send_keys(P)
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn_medium')]").click()
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//html").get_attribute("innerText")
            print(body)
        return body

    def expedia_explicit_wait(self):
        """
        :return: search result from expedia website
        """
        base_url = "https://www.expedia.com.sg"
        self.driver.implicitly_wait(1)
        self.driver.get(base_url)
        try:
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, "//button[@id='tab-flight-tab-hp']").click()
            self.driver.implicitly_wait(1)
            self.driver.find_element(
                By.XPATH, "//input[@id='flight-origin-hp-flight']"
            ).send_keys("Hong Kong, Hong Kong SAR (HKG-Hong Kong Intl.)")
            self.driver.implicitly_wait(1)
            self.driver.find_element(
                By.XPATH, "//input[@id='flight-destination-hp-flight']"
            ).send_keys("Bologna, Italy (BLQ-Guglielmo Marconi)")
            self.driver.implicitly_wait(1)
            self.driver.find_element(
                By.XPATH, "//input[@id='flight-departing-hp-flight']"
            ).send_keys("26/07/2019")
            self.driver.implicitly_wait(1)
            return_date = self.driver.find_element(
                By.XPATH, "//input[@id='flight-returning-hp-flight']"
            )
            return_date.clear()
            return_date.send_keys("31/07/2019")
            self.driver.implicitly_wait(3)
            self.driver.find_element(
                By.XPATH,
                "//form[@id='gcw-flights-form-hp-flight']//button[contains(@class, 'gcw-submit')]"
            ).click()

            wait = WebDriverWait(
                self.driver, 8, poll_frequency=4,
                ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]
            )
            element = wait.until(
                ec.presence_of_element_located((By.XPATH, "//input[@id='stopFilter_stops-1']")))
            element.click()
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//html").get_attribute("innerText")
            print(body)
        return body

    def expedia_explicit_work(self):
        """
        :return: search result from expedia website
        """
        try:
            wait = WebDriverWait(
                self.driver, 8, poll_frequency=1,
                ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]
            )
            wait.until(
                ec.presence_of_element_located(
                    (By.XPATH, "//input[@id='stopFilter_stops-1']"))).click()
            wait.until(
                ec.presence_of_element_located(
                    (By.XPATH, "//input[@id='stopFilter_stops-2']"))).click()
            wait.until(
                ec.presence_of_element_located(
                    (By.XPATH, "//input[@id='airlineRowContainer_CX']"))).click()
            wait.until(
                ec.presence_of_element_located(
                    (By.XPATH, "//input[@id='airlineRowContainer_LH']"))).click()
            time.sleep(3)
        except WebDriverException:
            self.driver.quit()
            raise WebDriverException
        finally:
            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//html").get_attribute("innerText")
            print(body)
        return body


if __name__ == '__main__':
    START = time.time()
    HAND = handler('main', 'main')
    END = time.time()
    print("Time spent operating this lambda function: " + str(END - START) + " seconds")
