
from collections import namedtuple

from app.models.gift import Gift
from app.view_models.book import BookViewMode

MyGift = namedtuple("MyGift", ["id", "book", "wishes_count"])


class MyGifts:
    def __init__(self, gifts_of_mine: Gift, wish_count_list: dict):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        temp_gifts = []
        for gitf in self.__gifts_of_mine:
            my_gift = self.__matching(gitf)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count["isbn"]:
                count = wish_count["count"]
        r = {
             "id": gift.id,
             "book": BookViewMode(gift.book),
             "count": count

         }
        return r
        # my_gift = MyGift(gift.id, BookViewMode(gift.book), count)
        # return my_gift


class Gift:
    pass