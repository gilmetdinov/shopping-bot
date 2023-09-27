from .abstract_factory import AbstractFactory


class AbstractKeyboardFactory(AbstractFactory):
    """
    self.keyboards - enum of a tuple of keyboard function from handler.utils.keyboards
     and list of args needed for the method
    """

    def __init__(self, keyboards):
        super().__init__()
        self.keyboards = keyboards

    def get_keyboard(self, order_type: str, kwargs: dict = None):
        enum_info = self.get_attr(self.keyboards, order_type).value if self.get_attr(self.keyboards, order_type) \
            else None
        if enum_info is None:
            return None
        (function, args) = enum_info
        real_kwargs = self.get_real_kwargs(kwargs=kwargs or {}, args=args)
        return function(**real_kwargs) if real_kwargs is not None else None
