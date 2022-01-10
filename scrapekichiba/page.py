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
        self.soup = BeautifulSoup(res.content, 'html.parser')

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
        """吉場ページのSP履歴を取得する関数

        race_idは，[年][月][日][何レース目][開催場所id]で構成され，
        例えば，2022年1月10日7レース目中山競馬場のレースなら，202201100776になる．
        開催場所idはconstモジュールのPlaceChuoを参照

        Args:
            race_id (str): SP履歴を取得したいレースのid

        Raises:
            ValueError: SP履歴表を取得するのに用いているpd.read_htmlが
                エラーメッセージでNo tables found matching patternをはいた場合は
                空のpd.DataFrameを返し，そのほかの場合は，そのエラーをraiseする．

        Returns:
            pd.DataFrame: 取得したSP履歴表
        
        Examples:
            >>> SearchPage('http://www.kichiuma.net/php/search.php?race_id=202201100776&date=2022%2F1%2F10&no=7&id=76&p=sp').get_sp_history('202201100776')
        枠   馬    競 走 馬 名 SP調整  ... ※スピード指数履歴欄の詳細【1行目】⇒競馬場、距離【2行1列目】⇒スピード指数、【2行2列目上段】⇒前半スピード(先行)指数、【2行2列目下段】⇒後半3Fスピード(上がり)指数(注)中央競馬、海外競馬、ばんえい競馬のスピード指数履歴はございません。
                枠   馬    競 走 馬 名 SP調整  ...                                                                                                                          前々走                3走前               4走前              
        5走前
            0   1   1    ヴォーグマチネ    …  ...                                   中山1800良 72 -0 -5                                                                             中山1800良 82 10 -8   東京2100良 69 1 -9    新潟1800 良 79 9 -5
            1   1   2     ネオヒューズ    …  ...                                    東京1600良 76 2 -6                                                                              中山1800良 85 6 -2   東京1600稍 78 -3 2    東京1600稍 80 -3 4
            2   2   3   クラウドスケープ    …  ...                                   福島1700良 63 8 -18                                                                              新潟1800良 72 6 -8   中山1800重 80 7 -6   札幌1700 良 61 -4 -7
            3   2   4   テンウォークライ    △  ...                                    中山1800良 89 9 -1                                                                              札幌1700良 72 -3 1  函館1700良 61 5 -18   東京1600 良 72 7 -15
            4   3   5   シングンジョーイ    …  ...                                   札幌1700良 59 6 -20                                                                             福島1700稍 67 -1 -5  新潟1200良 68 -7 -1  中京2000良 60 21 -32
            5   3   6   アメリカンエール    …  ...                                  東京2100良 75 10 -14                                                                             東京1600稍 74 -0 -5    新潟1800良 83 6 0    福島1700稍 78 -2 6
            6   4   7    ペイシャジュン    …  ...                                  東京2100稍 80 14 -14                                                                            東京1600良 85 19 -13    中山1800良 87 5 0     中山1800不 81 0 0
            7   4   8   ワカミヤクオーレ    ○  ...                                  東京2000良 83 13 -11                                                                             東京2100稍 85 12 -8  中山2200良 72 7 -13    中山1800不 81 -4 5
            8   5   9       サルーテ    …  ...                                     中山1800不 87 4 2                                                                              新潟1800良 75 -7 7   東京1600重 84 5 -0    東京1600稍 78 3 -4
            9   5  10   ウインジョイフル    ▲  ...                                     福島1700良 76 1 0                                                                             中山1800良 85 14 -9   新潟1800良 71 1 -4    新潟1800重 77 -5 7
            10  6  11  サトノパーシヴァル    △  ...                                  阪神2200良 33 37 -72                                                                             新潟1800良 61 4 -15               NaN              
        NaN
            11  6  12    カンリンポチェ    ◎  ...                                    新潟1800不 79 -4 9                                                                              福島1700良 78 -5 9  中山1800良 84 -6 10  中山1800良 47 -3 -25
            12  7  13  マサカウマザンマイ    …  ...                                   函館1700良 64 -3 -6                                                                             東京1600良 76 8 -12   東京1600稍 75 2 -6    東京1300稍 75 1 -6
            13  7  14      ダイモーン    △  ...                                    東京2100良 78 8 -9                                                                              東京2100稍 81 9 -8  中山1800重 88 11 -4  中山1800良 80 10 -10
            14  8  15       ロスコフ    …  ...                                   新潟1800不 83 10 -3                                                                             中山1800良 91 11 -0   函館1700良 75 2 -1   函館1700重 72 9 -12
            15  8  16   アララトテソーロ    …  ...                                     中京1800良 78 1 1                                                                              福島1700良 71 -5 1   新潟1800良 73 0 -1    東京1600不 77 3 -5
        """
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
