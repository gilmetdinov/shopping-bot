from .abstract_factory import AbstractFactory
from ..enums import ErrorCodes


class AbstractMessageFactory(AbstractFactory):

    """
    self.builder - messages.Builder class object
    self.messages - enum of a tuple of message method from messages.Builder class and list of args needed for the method
    self.errorMessage - a tuple of a method name from messages.Builder for an error and list of needed args
    """
    def __init__(self, builder, messages):
        super().__init__()
        self.builder = builder
        self.messages = messages
        self.errorMessage = ('error_message', ['code'])

    def get_message(self, order_type: str, kwargs: dict = None):
        enum_info = self.get_attr(self.messages, order_type).value \
            if self.get_attr(self.messages, order_type) else None
        method_name, args = enum_info or self.errorMessage
        method = self.get_attr(self.builder, method_name)
        kwargs = {'code': ErrorCodes.Unexpected.value} if method_name == 'error_message' else kwargs
        real_kwargs = self.get_real_kwargs(kwargs=kwargs or {}, args=args)
        return method(**real_kwargs) if real_kwargs is not None else None
