
from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):

    # 交易状态
    _pending = Column("pending", SmallInteger, default=1)

    # 邮寄信息
    create_time = Column("create_time", Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(100))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 返回枚举类型
    @property
    def pending(self):
        return PendingStatus(self._pending)

    # 返回枚举数字
    @pending.setter
    def pending(self, status):
        self._pending = status.value

    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())
    #
    # @property
    # def create_datetime(self):
    #     return datetime.fromtimestamp(self.create_time) if self.create_time else None
