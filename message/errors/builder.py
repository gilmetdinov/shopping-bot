from utils.enums import ErrorCodes


class ErrorMessageBuilder:

    def __init__(self, support_tg, settings_url):
        self.errorCodes = ErrorCodes
        self.supportTg = support_tg
        self.settingsUrl = settings_url

    def get_message_by_code(self, code):

        # 1
        if code == self.errorCodes.InvalidBindKey.value:
            return (f"Ключ указан неверно.\n"
                    f"Пожалуйста, проверьте, правильность введенных данных.", True)

        # 2
        elif code == self.errorCodes.ProfileAlreadyBound.value:
            return (f"Ваш профиль уже привязан к данному телеграм аккаунту\.\n"
                    f"Если Вы хотите отвязать аккаунт, вы можете воспользоваться "
                    f"[данной инструкцией]({self.settingsUrl})\.", False)

        # 3
        elif code == self.errorCodes.AccountAlreadyBound.value:
            return (f"Данный телеграм аккаунт уже привязан к профилю на сайте\.\n"
                    f"Если вы хотите отвязать аккаунт, вы можете воспользоваться "
                    f"[данной инструкцией]({self.settingsUrl})\.", False)

        # 4
        elif code == self.errorCodes.InvalidUnbindCode.value:
            return (f"Введенный код некорректный!\n"
                    f"Пожалуйста, удостоверьтесь в правильности введенных данных и попробуйте снова.\n\n"
                    f"Если у Вас возникли трудности с получением/введением кода для отвязки профиля, "
                    f"пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", True)
        # 5
        elif code == self.errorCodes.NotEnoughFunds.value:
            return f"Недостаточно средств для совершения заказа!", True

        # 6
        elif code == self.errorCodes.InvalidOrderData.value:
            return (f"Некорректные данные в заказе!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", True)

        # 7
        elif code == self.errorCodes.DataNotAvailable.value:
            return (f"К сожалению, на данный момент запрошенных данных нет в наличии.\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", True)
        # 8
        elif code == self.errorCodes.EmptyOrderList.value:
            return f"К сожалению, у Вас не найдено ни одного заказа.", True

        # 9
        elif code == self.errorCodes.OrderNotFound.value:
            return f"Заказ не найден.", False

        # 10
        elif code == self.errorCodes.Unbound.value:
            return f"Недоступно.", False

        # -2
        elif code == self.errorCodes.ApiError.value:
            return (f"Ошибка выполнения запроса!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: "
                    f"{self.supportTg}", True)

        # -3
        elif code == self.errorCodes.SignError.value:
            return (f"Ошибка валидации запроса!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: "
                    f"{self.supportTg}", True)

        # -4
        elif code == self.errorCodes.WalletCreateError.value:
            return (f"Ошибка создания кошелька для оплаты!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: "
                    f"{self.supportTg}", True)

        # -5
        elif code == self.errorCodes.EmptyServiceList.value:
            return (f"Не удалось получить список товаров!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", True)

        # -6
        elif code == self.errorCodes.GetBalanceError.value:
            return (f"Ошибка получения баланса!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", False)

        # - 7
        elif code == self.errorCodes.UploadError.value:
            return (f"Ошибка загрузки изобраения!\n"
                    f"Пожалуйста, обратитесь в нашу поддрежку: {self.supportTg}", False)

        # -8
        elif code == self.errorCodes.UnbindCodeError.value:
            return (f"Ошибка создания кода для отвязки!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", False)

        # -9
        elif code == self.errorCodes.PassportError.value:
            return (f"Ошибка получения данных для идентификации!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: {self.supportTg}", True)

        # -20 (internal for callback queries)
        elif code == self.errorCodes.InlineError.value:
            return (f"Возникла непредвиденная ошибка!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: "
                    f"{self.supportTg}", False)

        # -1 and other
        elif code != self.errorCodes.NoErrors.value:
            return (f"Возникла непредвиденная ошибка!\n"
                    f"Пожалуйста, обратитесь в нашу поддержку: "
                    f"{self.supportTg}", True)

    def get_incorrect_command_message(self, is_bind: bool = True):
        message = f"Некорректное использование команды\."
        message += f"\nИнструкция по привязке аккаунта доступна на нашем [сайте]({self.settingsUrl})\." \
            if is_bind else ""
        return message, False

    @classmethod
    def get_incorrect_input_message(cls):
        return f"Не удалось распознать Ваш ответ.", False
