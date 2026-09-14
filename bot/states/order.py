from aiogram.fsm.state import StatesGroup, State


class Order(StatesGroup):
    # выбор типа заказа (услуга/товар/товар B/товар C)
    choosingType = State()
    choosingProductCategory = State()
    # 2 шаг выбора: услуги/товара/товара B/товара C
    choosingHandler = State()
    choosingProduct = State()
    choosingProductB = State()
    choosingProductC = State()
    # формы заказа
    serviceForm = State()
    productForm = State()
    product_bForm = State()
    product_cForm = State()
    # доп шаги заказа услуги
    inputProductNumber = State()
    setHandler = State()
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
            cls.serviceForm,
            cls.productForm,
            cls.product_bForm,
            cls.product_cForm
        ]

    @classmethod
    def get_discrete_forms(cls) -> list:
        return [
            cls.productForm,
            cls.product_bForm,
            cls.product_cForm
        ]

    @classmethod
    def get_delivery_forms(cls) -> list:
        return [
            cls.product_bForm,
            cls.product_cForm
        ]
