from enum import Enum


class ErrorCodes(Enum):
    InlineError = -20
    PassportError = -9
    UnbindCodeError = -8
    UploadError = -7
    GetBalanceError = -6
    EmptyServiceList = -5
    WalletCreateError = -4
    SignError = -3
    ApiError = -2
    Unexpected = -1
    NoErrors = 0
    InvalidBindKey = 1
    ProfileAlreadyBound = 2
    AccountAlreadyBound = 3
    InvalidUnbindCode = 4
    NotEnoughFunds = 5
    InvalidOrderData = 6
    DataNotAvailable = 7
    EmptyOrderList = 8
    OrderNotFound = 9
    Unbound = 10
