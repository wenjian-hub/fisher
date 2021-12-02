
from datetime import datetime
from .base import db, Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship


class Wish(Base):
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