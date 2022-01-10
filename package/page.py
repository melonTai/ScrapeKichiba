# selenium
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# beautifulsoup
from bs4 import BeautifulSoup
import bs4

# request
import requests

# 標準モジュール
import time
import re
import traceback

# pandas
import pandas as pd

# numpy
import numpy as np

# const
from .const import Race

class BasePageRequest(object):
    """
    各ページクラスのベース
    特に，UI操作を必要としない(seleniumを使わない)，値を取得するだけのページのベースとして用いる
    """                         
    def __init__(self,url:str):
        """request用のベースクラス

        Args:
            url (str): url
        """
        self.update_url(url)

    def update_url(self, url):
        self.url = url
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        header = {
            'User-Agent': user_agent
        }
        try:
            res = requests.get(self.url, headers=header, timeout=30)
        except requests.exceptions.ConnectionError as e:
            time.sleep(30)
            res = requests.get(self.url, headers=header, timeout=30)
        self.soup = BeautifulSoup(res.content.decode("euc-jp", "ignore"), 'html.parser')

class BasePageSelenium(object):
    """
    各ページクラスのベース
    特に，UI操作を必要とする(seleniumを使う)，ページのベースとして用いる

    Args:
        object ([type]): [description]
    """
    def __init__(self, driver:WebDriver):
        """selenium用ベースクラスのコンストラクタ

        Args:
            driver (WebDriver): webDriver
        """
        self.driver = driver
        self.url = driver.current_url
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
    
    def update_url(self, url:str):
        self.driver.implicitly_wait(20)
        self.driver.get(url)
        self.url = self.driver.current_url
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def close(self):
        self.driver.close()

    
class SearchPage(BasePageRequest):
    """例：http://www.kichiuma.net/php/search.php?race_id=202201100776&date=2022%2F1%2F10&no=7&id=76&p=sp

    Args:
        BasePageRequest (object): seleniumを使わないでスクレイピングするページのベースクラス
    """

    def get_sp_history(self, race_id:str):
        race = Race()
        race.from_id(race_id)
        url = f"http://www.kichiuma.net/php/search.php?race_id={race_id}&date={race.year}%2F{int(race.month)}%2F{int(race.day)}&no={int(race.r)}&id={race.place}&p=sp"
        self.update_url(url)
        try:
            dfs = pd.read_html(str(self.soup), match="枠")
            df = dfs[0]
            return df
        except ValueError as e:
            message = "".join(traceback.format_exception_only(type(e), e))
            if "No tables found matching pattern" in message:
                return pd.DataFrame()
            else:
                raise ValueError(e)
