import requests
from bs4 import BeautifulSoup
from isbnlib.dev import stdmeta
from isbnlib.dev._exceptions import NoDataForSelectorError

class Book:
    LANGUAGE_MAP = {"Engels": "en", "Nederlands": "nl", "Duits": "de"}

    def __init__(self, isbn, html):
        self.html = html
        self.specs = {}
        self.isbn = isbn
        self.parse_specs()

    @property
    def title(self):
        return self.html.find("h1", class_="pdp-header__title").text.strip()

    @property
    def authors(self):
        for key in ["Auteur", "Redacteur"]:
            authors = self.specs.get(key, None)
            if authors:
                return authors.split("\n")
        return []

    @property
    def publisher(self):
        return self.specs.get("Uitgever", None)

    @property
    def year(self):
        date = self.specs.get("Verschijningsdatum", None)
        if date:
            try:
                year = re.match(r'.*(\d{4}).*', date).group(1)
            except:
                return None
            else:
                return int(year)
        return None

    @property
    def language(self):
        lang = self.specs.get("Taal", None)
        if lang in self.LANGUAGE_MAP:
            return self.LANGUAGE_MAP[lang]
        else:
            print(f"Warning: language {lang} not found in mapping")
            return lang

    def as_record(self):
        return {"Title": self.title,
                "Authors": self.authors,
                "Year": self.year,
                "Publisher": self.publisher,
                "Language": self.language,
                "ISBN-13": self.isbn}

    def parse_specs(self):
        specs_lists = self.html.find_all("dl", class_="specs__list")
        for specs_list in specs_lists:
            keys = [el.text.strip() for el in specs_list.find_all("dt")]
            values = [el.text.strip() for el in specs_list.find_all("dd")]
            specs_dict = dict(zip(keys, values))
            self.specs.update(specs_dict)


    def __str__(self):
        return f"""Title: {self.title}
Author: "; ".join({self.authors})
Publisher: {self.publisher}
Year: {self.year}
Language: {self.language}
ISBN: {self.isbn}"""

    def __repr__(self):
        return self.__str__()

    @classmethod
    def find(cls, isbn):
        url = "https://www.bol.com/nl/rnwy/search.html"
        r = requests.get(url, params={"Ntt": isbn})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return Book(isbn, soup)
        else:
            return None


def query(isbn):
    book = Book.find(isbn)
    if book:
        return book.as_record()
    else:
        raise NoDataForSelectorError(isbn)
