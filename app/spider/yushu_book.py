import json

from flask import current_app

from app.libs.httper import HTTP


class YuShuBook:
    # 模型层 MVC M层
    isbn_url = "http://t.talelin.com/v2/book/isbn/{}"
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []

    def __fill_single(self, data) -> json:
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data["total"]
        self.books = data["books"]

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.calculate_page(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def calculate_page(self, page):
        return (page-1) * current_app.config["PER_PAGE"]

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

