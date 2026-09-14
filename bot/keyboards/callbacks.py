from enum import Enum


class Callbacks(Enum):
    # common
    ConfirmOrder = 'confirm-order'
    GoBack = 'go-back'
    # pagination
    Page = 'page'
    FlipBack = 'flip-back'
    FlipForward = 'flip-forward'
    # service form
    InputProduct = 'input-product'
    ChooseHandler = 'choose-service'
    ChooseDocs = 'choose-docs'
    PrioritySwitch = 'priority-switch'
    UploadDocs = 'upload-docs'
    ViewDocs = 'view-docs'
    # product_b/product_c form
    InputAddress = 'input-address'
    InputFullName = 'input-full-name'
    InputPhoneNumber = 'input-phone-number'
    InputTelegram = 'input-telegram'
    ChooseDeliveryType = 'choose-delivery-type'
    # common form
    ChangeAmount = 'change-amount'
    # order info
    ViewData = 'view-data'
    Done = 'done'

