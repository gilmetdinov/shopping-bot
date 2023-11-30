from enum import Enum
from utils.enums import DeliveryType


class KeyboardEnum(Enum):
    order = ['🛒 Оформить заказ', '📚 Мои заказы']
    orderType = {
        'ident': '👤 Идентификация',
        'wallet': '💰 Готовый кошелек',
        'bundle': '📦 Комплект (Кошелек + карта)',
        'debit': '💳 Дебетовая карта'
    }
    orderListType = {
        'ident': '👤 Идентификации',
        'wallet': '💰 Готовые кошельки',
        'bundle': '📦 Комплекты'
    }
    walletCategory = ['Все', '💰 ЭПС', '🇪🇺 EU']
    replenish = ['💵 Пополнить баланс ']
    replenishmentMethod = ['BTC', 'ETH', 'LTC', 'USDT TRC-20', 'USDT ERC-20']
    settings = ['⚙️ Настройки']
    settingsMenu = {
        'refill': 'Уведомления о пополнении баланса: ',
        'order': 'Уведомления о выполненных заказах: '
    }
    toMain = ['🏠 На главную']
    goBack = ['↩️ Назад']
    goBackDict = {'go-back': '↩️ Назад'}
    done = ['🆗 Готово']
    viewData = ['ℹ️ Посмотреть данные']
    confirmation = ['✅ Да', '❌ Нет']
    pagination = {'flip-back': '⬅️', 'page': '', 'flip-forward': '➡️'}
    deliveryType = {
        DeliveryType.PickUpPoint.value: 'Доставка до ПВЗ (пункт выдачи СДЭК)',
        DeliveryType.DirectDelivery.value: 'Доставка до квартиры'
    }
    docsType = {
        1: 'Покупка данных',
        4: 'Покупка текст. данных',
        0: 'Ваши данные',
        3: 'Ваши текст. данные'
    }
    # словари с шортнеймами товаров/услуг из бд
    # нерелевантные, перемещено в бд
    identType = {
        'qw': '🥝 QIWI',  # moved
        'ya': '🟣 Юмани',  # moved
        '1c': '1️⃣ Цупис'  # moved
    }
    walletType = {
        'wallet_1': '🥝 QIWI Проф',  # moved
        'wallet_2': '🥝📱 QIWI договор + сим-карта',  # moved
        'wallet_3': '🥝 QIWI основной Без Сим-карты + API',  # moved
        'wallet_4': '🅿️ PAYEER',  # moved
        'wallet_5': '💵 AdvCash',  # moved
        'wallet_6': '🟣 Юмани',  # moved
        'wallet_7': '💵 WebMoney формальный',  # moved
        'wallet_8': '🅾️ OZON Виртуальная карта',  # moved
        'wallet_9': '💰 Capitalist',  # moved
        'wallet_12': '🌈 Payoneer',  # moved
        'wallet_13': '🅿️ PayPal',  # moved
        'wallet_18': '🇰🇿 QIWI КЗ полный вериф',  # moved
        "wallet_20": "💱 Binance",  # moved
        "wallet_21": "💱 bitnovo",  # moved
        "wallet_22": "💱 bitpay.com",  # moved
        "wallet_23": "💱 bitzlato.com",  # moved
        "wallet_25": "💱 btc-alpha.com",  # moved
        'wallet_27': '🇪🇺 coinbase EU',  # moved
        "wallet_28": "💱 coinmama.com",  # moved
        "wallet_29": "💱 Coinpayments",  # moved
        "wallet_30": "💱 CoinsBank",  # moved
        "wallet_31": "💱 crypto.com",  # moved
        "wallet_32": "💱 exmo.me",  # moved
        "wallet_34": "💱 Hitbtc.com",  # moved
        "wallet_35": "💱 koinal.io",  # moved
        'wallet_36': '🇪🇺 Kraken',  # moved
        "wallet_37": "💱 kucoin.com",  # moved
        "wallet_38": "💱 Localbitcoins T1",  # moved
        "wallet_39": "💱 Localbitcoins T2",  # moved
        "wallet_40": "💱 mercuryo.io",  # moved
        "wallet_41": "💱 okcoin",  # moved
        "wallet_43": "💱 Poloniex",  # moved
        "wallet_44": "💱 Uphold",  # moved
        "wallet_46": "💱 Wirex",  # moved
        'wallet_48': '🥝 QIWI минимальный',  # moved
        "wallet_49": "cex.io",  # moved
        'wallet_52': '🥝 QIWI основной',  # moved
        "wallet_55": "cryptopay.me",  # moved
        'wallet_58': '🇪🇺 Advcash EU + VCC',  # moved
        "wallet_59": "Nebeus",  # moved
        "wallet_63": "blockchain.com",  # moved
        "wallet_64": "Skrill",  # moved
        "wallet_66": "Paxful",  # moved
        "wallet_67": "Onlyfans",  # moved
        "wallet_68": "Google Voice",  # moved
        'wallet_70': '🇪🇺 Airbnb EU',  # moved
        'wallet_71': '🇪🇺 Binance EU',  # moved
        "wallet_72": "🇺🇸 Binance US",  # moved
        'wallet_73': '🇪🇺 Crypto.com EU',  # moved
        'wallet_74': '🇪🇺 Localbitcoins T2 EU',  # moved
        'wallet_75': '🇪🇺 Paxful EU',  # moved
        'wallet_76': '🇪🇺 Skrill EU',  # moved
        'wallet_77': '🇪🇺 cex.io EU',  # moved
        "wallet_78": "💱 Crypterium",  # moved
        'wallet_79': '🇪🇺 blockchain.com EU',  # moved
        'wallet_82': '🌸 Piastrix',  # moved
        'wallet_83': '🇪🇺 Atmen EU + VCC',  # moved
        'wallet_84': '🇪🇺 Blackcatcard EU + VCC',  # moved
        'wallet_85': '🇪🇺 Bunq EU+ VCC',  # moved
        'wallet_86': '🇪🇺 Capitalist EU + VCC',  # moved
        'wallet_87': '🇪🇺 Coinmama EU',  # moved
        'wallet_88': '🇪🇺 Coinpayments EU',  # moved
        'wallet_89': '🇪🇺 Coinpayments EU',  # moved
        'wallet_90': '🇪🇺 Cryptopay EU + VCC',  # moved
        'wallet_91': '🇪🇺 Curve EU + VCC',  # moved
        'wallet_92': '🇪🇺 Anycoindirect EU',  # moved
        'wallet_93': '🇪🇺 Crypterium EU',  # moved
        "wallet_94": "💱 Huobi",  # moved
        'wallet_95': "Bybit СНГ",  # moved
        'wallet_96': 'Kukoin СНГ',  # moved
        'wallet_97': '🇪🇺 Bybit EU'  # moved
    }
    bundleType = {
        'qw_sim': '📱 QIWI Проф Без карты',  # moved
        'qw': '💳 QIWI проф + Неименная карта',  # moved
        'qw_big': '👑 QIWI Premium',  # moved
        'paypal': '🅿️ PayPal',  # moved
        'qw_ozon': '🥝🅾️ QIWI + OZON',  # moved
        'qw_yoomoney': '🥝🟣 QIWI + ЮMoney',  # moved
        'qw_ozon_yoomoney': '🥝🅾️🟣 QIWI + OZON + ЮMoney'  # moved
    }
    debitType = {
        'qw_noname': 'QIWI неименная',
        'tink_plat': 'Тинькофф',
        'altyn-i': 'Алтын банк Казахстан',
        'raif_gold_visa': 'Райффайзен',
        'alfa_basic': 'Альфа Банк',
        'avangard': 'Авангард',
        'vost_moment': 'Восточный',
        'vtb_plat': 'ВТБ',
        'gazprom': 'Газпром',
        'otkritie': 'Открытие',
        'rosbank': 'Росбанк',
        'sovkom': 'Совкомбанк',
        'uralsib': 'Уралсиб',
        'otp_bank': 'ОТП Банк',
        'sber': 'Сбербанк'
    }
