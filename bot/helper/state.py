from bot import states


class StateHelper:
    """Gets different lists of states to ease setting routes with decorators"""

    def __init__(self):
        self.states = states

    def order_form_states(self):
        """List of all form states"""
        return self.states.Order.get_forms()

    def discrete_order_form_states(self):
        """List of form states for quantiable order types (product, product_b, product_c)"""
        return self.states.Order.get_discrete_forms()

    def delivery_order_form_states(self):
        """List of form states for delivery order types (product_b, product_c)"""
        return self.states.Order.get_delivery_forms()

    def paginated_step_two_lists(self):
        return [
            self.states.Order.choosingProductC
        ]

    def choosing_order_states(self, _true=False):
        """Basically list of step two states except service
        :param _true: if True, then returns real service choosing states, else returns states of common step two"""
        return [
            self.states.Order.choosingProduct if _true else self.states.Order.choosingProductCategory,
            self.states.Order.choosingProductB,
            self.states.Order.choosingProductC
        ]

    def to_main_page_states(self):
        """List of states from which it is possible to go to main page with GoBack reply markup button"""
        return [
            self.states.Settings.menu,
            self.states.Order.choosingType,
            self.states.List.choosingType
        ]
