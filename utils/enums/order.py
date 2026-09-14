from enum import Enum


class OrderStatus(Enum):
    error = -2
    cancelled = -1
    new = 3
    sentToHandler = 4
    complete = 5
