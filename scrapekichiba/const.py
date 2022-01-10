import re
from enum import Enum

class PlaceChuo(Enum):
    """中央競馬における各レース場のid

    Args:
        Enum (int): レース場に割り当てられたid
            吉場サイトにアクセスする際のurl中で使用される．
    """
    Sapporo = 71
    Hakodate = 72
    Fukushima = 73
    Nigata = 74
    Tokyo = 75
    Nakayama = 76
    Tyukyo = 77
    Kyoto = 78
    Hanshin = 79
    Ogura = 80

class Race():
    """レース情報を格納するクラス．

    あるレースのid，開催年月日，何レース目か，レース場idを格納する．
    また，idから上記パラメータ．パラメータからidの変換も行う．

    """
    def __init__(self):
        self.id = None #: str: レース場id
        self.year = None#: int: 開催年
        self.month = None#: int: 開催月
        self.day = None#: int: 開催日
        self.r = None#: int: 何レース目か
        self.place = None#: int: レース場id

    def from_id(self,id):
        """レースidから開催年月日，何レース目，レース場idを抽出し，propertyに保存する．

        Args:
            id (str): レースid

        Raises:
            Exception: idのフォーマットが誤っている可能性がある場合に投げられる．
        
        Examples:
            >>> Race().from_id('202201100776')
            (2022, 1, 10, 7, 76)
        """
        self.id = id
        pattern = "(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})"
        match = re.findall(pattern, id)
        if match:
            year, month, day, r, place = match[0]
            self.year = int(year)
            self.month = int(month)
            self.day = int(day)
            self.r = int(r)
            self.place = int(place)
            return self.year, self.month, self.day, self.r, self.place
        else:
            raise Exception(f"invalid race_id {self.id}")

    def from_param(self, year:int, month:int, day:int, r:int, place:int):
        """レースの開催年月日，何レース目か，レース場idからレースidを生成する．

        Args:
            year (int): 開催年
            month (int): 開催月
            day (int): 開催日
            r (int): 何レース目
            place (int): レース場id

        Returns:
            str: レースid
        
        Examples:
            >>> Race().from_param(2022, 1, 10, 7, 76)
            '202201100776'
        """
        self.id = f"{year:04}{month:02}{day:02}{r:02}{place:02}"
        self.year = year
        self.month = month
        self.day = day
        self.r = r
        self.place = place
        return self.id

if __name__ == '__main__':
    import doctest
    doctest.testmod()