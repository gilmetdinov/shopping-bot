class FactoryHelper:
    @classmethod
    def get_attribute(cls, obj, attr):
        try:
            return getattr(obj, attr)
        except AttributeError:
            return None
