"""
Simple Usage with headless chrome
AWS lambda layers are located at /opt/ directory.
Note that env will never be commited remotely
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from env import (USERNAME, PASSWORD)


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
                "browser interation": sele.steam_browser_interactions(),
                "click send": sele.steam_click_keys(),
                "element state": sele.steam_element_state(),
                "radio checkbox": sele.steam_radio_checkbox(),
                "element list": sele.steam_element_list(),
                "dropdown element": sele.steam_dropdown_element(),
                "hidden element": sele.steam_hidden_elements()
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

    def steam_browser_interactions(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            title = self.driver.title
            print("Title of the webpage is: " + title)
            print("Current Url of the web page is: " + self.driver.current_url)
            self.driver.refresh()
            print("Browser Refreshed 1st time")
            self.driver.get(self.driver.current_url)
            print("Current Url of the web page is: " + self.driver.current_url)
            print("Browser Refreshed 2nd time")
            self.driver.get("https://steamcommunity.com/")
            print("Current Url of the web page is: " + self.driver.current_url)
            self.driver.back()
            print("Go one step back in browser history")
            print("Current Url of the web page is: " + self.driver.current_url)
            self.driver.forward()
            print("Go one step forward in browser history")
            self.driver.back()
            print("Current Url of the web page is: " + self.driver.current_url)

            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def steam_click_keys(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            self.driver.find_element(By.XPATH, "//a[@class='global_action_link']").click()
            self.driver.find_element(
                By.XPATH, "//input[@id='input_username']"
            ).send_keys(USERNAME)
            self.driver.find_element(
                By.XPATH, "//input[@id='input_password']"
            ).send_keys(PASSWORD)
            self.driver.find_element(
                By.XPATH, "//button//span[contains(text(), 'Sign in')]"
            ).click()
            self.driver.implicitly_wait(2)
            self.driver.find_element(By.XPATH, "//span[@id='account_pulldown']").click()
            self.driver.find_element(
                By.XPATH, "//a[@class='popup_menu_item'][contains(text(),'Account details')]"
            ).click()

            self.driver.implicitly_wait(2)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def steam_element_state(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            elems = self.driver.find_elements(By.XPATH, "//a")
            for ele in elems:
                if ele.is_enabled() and ele.is_displayed():
                    print(ele.get_attribute("innerText").strip())

            self.driver.implicitly_wait(4)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def steam_radio_checkbox(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/search"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            tags = self.driver.find_elements(By.XPATH, "//div[@id='narrow_category1']//div")
            print("tags: " + str(len(tags)))
            tag_see_all = self.driver.find_element(
                By.XPATH, "//div[@id='additional_search_options']//div[2]//a[1]")
            self.driver.implicitly_wait(1)
            tag_see_all.click()
            for tag in tags:
                if tag.is_enabled() and tag.is_displayed():
                    self.driver.implicitly_wait(1)
                    tag.click()
                    self.driver.implicitly_wait(1)
                    body = self.driver.find_element(
                        By.XPATH, "//div[@id='search_results']").get_attribute("innerText")
                    print(body)
                    if tag.is_selected():
                        tag.click()

            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def steam_element_list(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/search"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            tags = self.driver.find_elements(
                By.XPATH,
                "//div[contains(text(),'Narrow by number of "
                "players')]/../following-sibling::div//div")
            print("tags: " + str(len(tags)))
            self.driver.implicitly_wait(1)
            for tag in tags:
                if tag.is_enabled() and tag.is_displayed():
                    self.driver.implicitly_wait(1)
                    tag.click()
                    self.driver.implicitly_wait(1)
                    body = self.driver.find_element(
                        By.XPATH, "//div[@id='search_results']").get_attribute("innerText")
                    print(body)
                    if tag.is_selected():
                        tag.click()

            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def steam_dropdown_element(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/search"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            action = ActionChains(self.driver)
            first_menu = self.driver.find_element(By.XPATH, "//a[contains(text(),'STORE')]")
            action.move_to_element(first_menu).perform()
            second_menu = self.driver.find_element(
                By.XPATH, "//div[@class='supernav_content']//a[contains(text(),'Stats')]")
            second_menu.click()

            self.driver.implicitly_wait(1)
            body = self.driver.find_element(By.XPATH, "//body").get_attribute("innerText")
            print(body)
        except WebDriverException:
            self.driver.close()
            self.driver.quit()
            raise WebDriverException
        return body

    def steam_hidden_elements(self):
        """
        :return: search result from steam website
        """
        base_url = "https://store.steampowered.com/search"
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.implicitly_wait(1)
        try:
            eles = self.driver.find_elements(By.XPATH, "//html//*[string-length(text())>0]")
            for ele in eles:
                if ele.is_displayed():
                    print(ele.get_attribute("innerText"))

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
