from enum import Enum
from bot.handler.processes.order import *
from bot.handler.services.order import *


class OrderProcesses(Enum):
    ident = IdentProcess
    wallet = WalletProcess
    bundle = BundleProcess
    debit = DebitProcess


class OrderServices(Enum):
    ident = IdentService
    wallet = WalletService
    bundle = BundleService
    debit = DebitService
