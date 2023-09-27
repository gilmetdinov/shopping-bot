from enum import Enum


class Callbacks(Enum):
    # common
    ConfirmOrder = 'confirm-order'
    GoBack = 'go-back'
    # pagination
    Page = 'page'
    FlipBack = 'flip-back'
    FlipForward = 'flip-forward'
    # ident form
    InputWallet = 'input-wallet'
    ChooseService = 'choose-service'
    ChooseDocs = 'choose-docs'
    PremiumSwitch = 'premium-switch'
    UploadDocs = 'upload-docs'
    ViewDocs = 'view-docs'
    # bundle/debit form
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

