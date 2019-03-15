from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import requests
import sys

from config import Config


class EmailChecker:

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '185.121.139.55',
                    "proxy_port": '21186'}

    def __init__(self):

        self.cred = self._get_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--incognito")
        options.add_argument('--proxy-server=socks://' + self.cred['proxy_host'] + ':' + self.cred['proxy_port'])

        # self.driver = webdriver.Chrome(chrome_options=options)

        # remote webdriver
        self.driver = webdriver.Remote(
            command_executor='http://' + Config.SELENIUM_CONFIG['host'] + ':' + Config.SELENIUM_CONFIG[
                'port'] + '/wd/hub',
            desired_capabilities=options.to_capabilities(),
        )

        self.EMAILFIELD = (By.NAME, "emailOrPhone")
        self.FULLNAME = (By.NAME, "fullName")

    def checker(self, emailId):
        url = "https://www.instagram.com/?hl=en"
        self.driver.get(url)
        sleep(0.1)
        # # print(emailId)
        #
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EMAILFIELD)).send_keys(emailId)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.FULLNAME)).click()
        sleep(1)
        # self.driver.find_element_by_class_name('coreSpriteInputError gBp1f')
        try:
            self.driver.find_element_by_xpath('//span[@class="coreSpriteInputError gBp1f"]')
            self.driver.quit()
            return {'profileExists': True,
                    'profile': emailId}
        except:
            self.driver.quit()
            return {'profileExists': False}


if __name__ == '__main__':
    obj = EmailChecker()
    print(obj.checker('austinpaul134@outlook.com'))
    # obj.driver.quit()
# +919416284225