import re
from enum import Enum

class PlaceChuo(Enum):
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
    def __init__(self):
        self.id = None
        self.year = None
        self.month = None
        self.day = None
        self.r = None
        self.place = None

    def from_id(self,id):
        self.id = id
        pattern = "(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})"
        match = re.findall(pattern, id)
        if match:
            year, month, day, r, place = match[0]
            self.year = year
            self.month = month
            self.day = day
            self.r = r
            self.place = place
        else:
            raise Exception(f"invalid race_id {self.id}")

    def from_param(self, year, month, day, r, place):
        self.id = f"{year:04}{month:02}{day:02}{r:02}{place:02}"
        self.year = year
        self.month = month
        self.day = day
        self.r = r
        self.place = place