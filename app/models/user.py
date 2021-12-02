from datetime import datetime
from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from app import login_manager
from app.models.book import Book
from app.models.gift import Gift
from app.models.wish import Wish
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    """
    __tablename__ = "user1"  指定表名
    _password = Column("password")  将_password指定成password
    """
    id = Column(Integer, primary_key=True)
    nickname = Column(String(21), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column("password", String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receiver_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """ check_password_hash  密码加密对比 """
        return check_password_hash(self._password, raw)

    """
    flask-login 识别用户身份信息，get_id为固定函数
     def get_id(self):
        return self.
        
     如果身份不是id变量，需要重写def get_id()方法
    """

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != "isbn":
            return False

        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 既不在赠送清单中也不再心愿清单中
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        return False if gifting or wishing else True


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))
