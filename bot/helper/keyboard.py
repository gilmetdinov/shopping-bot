class KeyboardHelper:

    @classmethod
    def key_value_reverse(cls, _dict: dict):
        new_dict = {}
        for key, value in _dict.items():
            new_dict[value] = key
        return new_dict

    @classmethod
    def get_price(cls, order: str) -> float:
        price = order.split('(')[1].strip('р.)')
        return float(price)
