import time
from loguru import logger
from utils import stopwatch
from loguru import logger

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

import os

is_headless = True

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'


class Chrome:
    def __init__(self, user=user_agent):
        logger.debug('Инициализирую объект Chrome')

        # Selenium
        os.environ['WDM_LOCAL'] = '1'
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--no-sandbox")
        self.option.add_argument("--log-level=3")
        # self.option.add_argument("--start-maximized")
        self.option.add_argument("--window-size=2560,1440")
        self.option.add_argument("--disable-gpu")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.option.add_argument(f"user-data-dir={os.getcwd()}/selenium")
        self.option.add_argument(f'user-agent={user}')
        self.option.headless = is_headless  # True - тихий режим (без интерфейса), False - с интерфейсом браузера
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.option)
        self.driver.set_page_load_timeout = 10

    @stopwatch
    def get_html(self, url):
        try:
            self.driver.get(url)
            time.sleep(3)
            source = self.driver.page_source

        except Exception:
            self.driver.quit()
            del self.driver

            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.option)
            self.driver.get(url)
            time.sleep(5)
            source = self.driver.page_source

        return source

    def quit(self):
        self.driver.quit()
        return 0