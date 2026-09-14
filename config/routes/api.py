from enum import Enum


class ApiRoutes(Enum):
    ping = '/api/telegram/'
    test = '/api/telegram/test'
    bind = '/api/telegram/bind'
    check_user = '/api/telegram/check-user'
    get_unbind_code = '/api/telegram/get-unbind-code'
    unbind = '/api/telegram/unbind'
    get_payment_address = '/api/telegram/get-payment-address'
    get_balance = '/api/telegram/get-balance'
    get_notif_settings = '/api/telegram/get-notif-settings'
    switch_notif = '/api/telegram/switch-notif'
    get_service_list = '/api/telegram/get-service-list'
    get_order_cache = '/api/telegram/get-order-cache'
    update_order_cache = '/api/telegram/update-order-cache'
    delete_images = '/api/telegram/delete-images'
    upload_image = '/api/telegram/upload-image'
    make_order = '/api/telegram/make-order'
    get_order_list = '/api/telegram/get-order-list'
    get_order_info = '/api/telegram/get-order-info'
    get_order_add_info = '/api/telegram/get-order-additional-info'
    search_order = '/api/telegram/search-order'
