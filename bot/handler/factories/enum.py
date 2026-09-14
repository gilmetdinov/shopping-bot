from enum import Enum
from bot.handler.processes.order import *
from bot.handler.handlers.order import *


class OrderProcesses(Enum):
    service = ServiceProcess
    product = ProductProcess
    product_b = ProductBProcess
    product_c = ProductCProcess


class OrderHandlers(Enum):
    service = ServiceHandler
    product = ProductHandler
    product_b = ProductBHandler
    product_c = ProductCHandler
