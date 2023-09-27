from aiogram.fsm.state import StatesGroup, State


class Order(StatesGroup):
    # выбор типа заказа (идент/кош/комплект/дебет)
    choosingType = State()
    choosingWalletCategory = State()
    # 2 шаг выбора: идента/кошелек/комплект/дебет
    choosingIdent = State()
    choosingWallet = State()
    choosingBundle = State()
    choosingDebit = State()
    # формы заказа
    identForm = State()
    walletForm = State()
    bundleForm = State()
    debitForm = State()
    # доп шаги заказа идента
    inputWalletNumber = State()
    setService = State()
    setDocs = State()
    uploadImageDocs = State()
    uploadStringDocs = State()
    viewingDocs = State()
    # доп шаги заказов
    inputAmount = State()
    inputAddress = State()
    inputFullName = State()
    inputPhoneNumber = State()
    inputTelegram = State()
    choosingDeliveryType = State()

    @classmethod
    def get_forms(cls) -> list:
        return [
            cls.identForm,
            cls.walletForm,
            cls.bundleForm,
            cls.debitForm
        ]

    @classmethod
    def get_discrete_forms(cls) -> list:
        return [
            cls.walletForm,
            cls.bundleForm,
            cls.debitForm
        ]

    @classmethod
    def get_delivery_forms(cls) -> list:
        return [
            cls.bundleForm,
            cls.debitForm
        ]
