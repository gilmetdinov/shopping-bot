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
    # словари с шортнеймами товаров/услуг из бд
    identType = {
        'qw': '🥝 QIWI',
        'ya': '🟣 Юмани',
        '1c': '1️⃣ Цупис'
    }
    docsType = {
        1: 'Покупка данных',
        4: 'Покупка текст. данных',
        0: 'Ваши данные',
        3: 'Ваши текст. данные'
    }
    walletType = {
        'wallet_1': '🥝 QIWI Проф',
        'wallet_2': '🥝📱 QIWI договор + сим-карта',
        'wallet_3': '🥝 QIWI основной Без Сим-карты + API',
        'wallet_4': '🅿️ PAYEER',
        'wallet_5': '💵 AdvCash',
        'wallet_6': '🟣 Юмани',
        'wallet_7': '💵 WebMoney формальный',
        'wallet_8': '🅾️ OZON Виртуальная карта',
        'wallet_9': '💰 Capitalist',
        'wallet_12': '🌈 Payoneer',
        'wallet_13': '🅿️ PayPal',
        'wallet_18': '🇰🇿 QIWI КЗ полный вериф',
        "wallet_20": "💱 Binance",
        "wallet_21": "💱 bitnovo",
        "wallet_22": "💱 bitpay.com",
        "wallet_23": "💱 bitzlato.com",
        "wallet_25": "💱 btc-alpha.com",
        'wallet_27': '🇪🇺 coinbase EU',
        "wallet_28": "💱 coinmama.com",
        "wallet_29": "💱 Coinpayments",
        "wallet_30": "💱 CoinsBank",
        "wallet_31": "💱 crypto.com",
        "wallet_32": "💱 exmo.me",
        "wallet_34": "💱 Hitbtc.com",
        "wallet_35": "💱 koinal.io",
        'wallet_36': '🇪🇺 Kraken',
        "wallet_37": "💱 kucoin.com",
        "wallet_38": "💱 Localbitcoins T1",
        "wallet_39": "💱 Localbitcoins T2",
        "wallet_40": "💱 mercuryo.io",
        "wallet_41": "💱 okcoin",
        "wallet_43": "💱 Poloniex",
        "wallet_44": "💱 Uphold",
        "wallet_46": "💱 Wirex",
        'wallet_48': '🥝 QIWI минимальный',
        "wallet_49": "cex.io",
        'wallet_52': '🥝 QIWI основной',
        "wallet_55": "cryptopay.me",
        'wallet_58': '🇪🇺 Advcash EU + VCC',
        "wallet_59": "Nebeus",
        "wallet_63": "blockchain.com",
        "wallet_64": "Skrill",
        "wallet_66": "Paxful",
        "wallet_67": "Onlyfans",
        "wallet_68": "Google Voice",
        'wallet_70': '🇪🇺 Airbnb EU',
        'wallet_71': '🇪🇺 Binance EU',
        "wallet_72": "🇺🇸 Binance US",
        'wallet_73': '🇪🇺 Crypto.com EU',
        'wallet_74': '🇪🇺 Localbitcoins T2 EU',
        'wallet_75': '🇪🇺 Paxful EU',
        'wallet_76': '🇪🇺 Skrill EU',
        'wallet_77': '🇪🇺 cex.io EU',
        "wallet_78": "💱 Crypterium",
        'wallet_79': '🇪🇺 blockchain.com EU',
        'wallet_82': '🌸 Piastrix',
        'wallet_83': '🇪🇺 Atmen EU + VCC',
        'wallet_84': '🇪🇺 Blackcatcard EU + VCC',
        'wallet_85': '🇪🇺 Bunq EU+ VCC',
        'wallet_86': '🇪🇺 Capitalist EU + VCC',
        'wallet_87': '🇪🇺 Coinmama EU',
        'wallet_88': '🇪🇺 Coinpayments EU',
        'wallet_89': '🇪🇺 Coinpayments EU',
        'wallet_90': '🇪🇺 Cryptopay EU + VCC',
        'wallet_91': '🇪🇺 Curve EU + VCC',
        'wallet_92': '🇪🇺 Anycoindirect EU',
        'wallet_93': '🇪🇺 Crypterium EU',
        "wallet_94": "💱 Huobi",
        'wallet_95': "Bybit СНГ",
        'wallet_96': 'Kukoin СНГ',
        'wallet_97': '🇪🇺 Bybit EU'
    }
    bundleType = {
        'qw_sim': '📱 QIWI Проф Без карты',
        'qw': '💳 QIWI проф + Неименная карта',
        'qw_big': '👑 QIWI Premium',
        'paypal': '🅿️ PayPal',
        'qw_ozon': '🥝🅾️ QIWI + OZON',
        'qw_yoomoney': '🥝🟣 QIWI + ЮMoney',
        'qw_ozon_yoomoney': '🥝🅾️🟣 QIWI + OZON + ЮMoney'
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
