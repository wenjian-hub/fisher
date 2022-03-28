"""
上下文管理器
"""
from contextlib import contextmanager


class MySource:

    @contextmanager
    def query(self, a):
        try:
            yield
            print("aaaa")
            return 5 / a
        except Exception as e:
            raise e


mysource = MySource()

with mysource.query(0) as r:
    print(12345)
    print("qwer")
    print(1234556)
