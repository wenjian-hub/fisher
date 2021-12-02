from datetime import datetime

from flask_login import UserMixin, current_user

from .base import db, Base
from sqlalchemy import Column, Integer, String


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
    create_time = Column("create_time", Integer, nullable=False)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        return datetime.fromtimestamp(self.create_time) if self.create_time else None

    # 写入书籍数据
    def can_book_date(self):
        isbn = Book.query.filter_by(current_user.isbn).first()
        print(isbn)
        return True if isbn else False
