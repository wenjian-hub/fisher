
from datetime import datetime
from app.models.base import db, Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, SmallInteger, desc, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    # Gift和User关联
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False, unique=True)
    launched = Column(Boolean, default=False, comment="礼物是否送出")
    create_time = Column("create_time", Integer, nullable=False)

    @classmethod
    def get_user_wishes(cls, uid):
        # 数据库模型查询
        wishes = Wish.query.filter_by(uid=uid, launched=False). \
            order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_count(cls, isbn_list):
        from app.models.gift import Gift
        # db.session.query
        # db.session 查询，查询的是一组模型
        # 返回的是数量
        count_list = db.session.query(func.count(Gift.id), Gift.isbn). \
            filter(Gift.launched == False, Gift.isbn.in_(isbn_list), Gift.status == 1). \
            group_by(Gift.isbn).all()
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list

    # 通过 isbn 获取书籍数据
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
