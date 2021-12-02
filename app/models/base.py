from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, BigInteger
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            # yield 中断，让函数跳转到 with auto_commit函数外的函数执行
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):

    # 重写 filter_by 后，如果需要用到原有功能，需要继承父类的方法
    def filter_by(self, **kwargs):
        if "status" not in kwargs.keys():
            kwargs["status"] = 1

        return super(Query, self).filter_by(**kwargs)


# flask 使用重写的 Query
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    """
    Base 继承db.Model, flask会默认把Base创建成表，但是表都会创建一个主键。
    __abstract__ = True, 告诉sqlalchemy，不创建Base表

    """
    # 数据库基类模型
    __abstract__ = True
    status = Column(SmallInteger, default=1)

    def set_attr(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)