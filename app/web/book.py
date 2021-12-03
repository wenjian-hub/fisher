from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from flask import request, jsonify, flash, render_template
from . import web
import json

from ..models.base import db
from ..models.book import Book
from ..models.gift import Gift
from ..models.wish import Wish
from ..view_models.book import BookCollection, BookViewMode
from ..view_models.trade import TradeInfo


@web.route('/book/search')
def search():
    """
        query :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        query = form.query.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(query)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(query)
        else:
            yushu_book.search_by_keyword(query, page)

        books.fill(yushu_book, query)

        """
        解析data中带object的对象
        data = {"key1":"value1", "key2":"value2", "key3": object}
        return json.dumps(books, default=lambda x: x.__dict__)
        """
    else:
        flash('查询有误，请重新输入')
        # return jsonify(form.errors)
    return render_template("search_result.html", books=books, form=form)


@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_gits = False
    has_in_wishes = False

    # 获取书籍数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewMode(yushu_book.first)

    if Book().save_book_data(isbn):
        with db.auto_commit():
            books = Book()
            books.title = book.title
            books.author = book.author
            books.binding = book.binding
            books.publisher = book.publisher
            books.price = book.price
            books.pages = book.pages
            books.pubdate = book.pubdate
            books.isbn = book.isbn
            books.summary = book.summary
            books.image = book.image
            db.session.add(books)

    # 判断用户是否登录
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gits = True

        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template("book_detail.html", book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gits=has_in_gits, has_in_wishes=has_in_wishes)


