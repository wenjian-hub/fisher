from app.models.gift import Gift


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods: Gift) -> dict:
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single: Gift) -> dict:
        return dict(
            user_name=single.user.nickname,
            time=single.create_datetime.strftime("%Y-%m-%d") if single.create_datetime else "未知",
            ig=single.id
        )
