from .factory_helper import FactoryHelper


class AbstractFactory:
    def __init__(self):
        self.helper = FactoryHelper

    @classmethod
    def get_real_kwargs(cls, kwargs: dict, args: list):
        real_kwargs = {}
        for arg in args:
            if arg in kwargs.keys():
                real_kwargs[arg] = kwargs[arg]
        if len(real_kwargs) != len(args):
            return None
        return real_kwargs

    def get_attr(self, obj, attr):
        return self.helper.get_attribute(obj, attr)
