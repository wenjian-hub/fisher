from datetime import datetime

from flask import current_app

from .base import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, desc
from sqlalchemy.orm import relationship

from ..spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)

    # Gift和User关联
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False, unique=True)
    launched = Column(Boolean, default=False, comment="礼物是否送出")
    create_time = Column("create_time", Integer, nullable=False)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        return datetime.fromtimestamp(self.create_time) if self.create_time else None

    # Gift和Book关联
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))

    # 通过 isbn 获取书籍数据
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    """
    礼物是所有的，不属于具体实例对象
    """
    @classmethod
    def recent(cls):
        """
        最近礼物：
        1. 只显示一定数量礼物  30个   limit
        2. 按照时间倒序排序   order by desc
        3. 去重，同一本书不能重复出现  distinct

        """
        # sql 语句为链式调用
        recent_gifts = Gift.query.filter_by(launched=False).\
            group_by(Gift.isbn).\
            order_by(desc(Gift.create_time)).\
            limit(current_app.config["RECENT_BOOK_COUNT"]).all()
        return recent_gifts