from datetime import datetime
from math import floor

from flask import current_app

from app.libs.enums import PendingStatus
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from app import login_manager
from app.models.book import Book
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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
    create_time = Column("created_time", Integer, nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """ check_password_hash  密码加密对比 """
        return check_password_hash(self._password, raw)

    # @property
    # def create_datetime(self):
    #     return datetime.fromtimestamp(self.create_time) if self.create_time else None

    """
    flask-login 识别用户身份信息，get_id为固定函数
     def get_id(self):
        return self.
        
     如果身份不是id变量，需要重写def get_id()方法
    """

    # 判断鱼漂, 收单两本书籍，必须送出一本书籍
    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

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

    # 生成token, token里包含用户的user_id
    def generate_token(self, expiration=600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        """伪造token, 过期token"""
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return e
        uid = data.get("id")
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + "/" + str(self.receiver_counter)
        )


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))
