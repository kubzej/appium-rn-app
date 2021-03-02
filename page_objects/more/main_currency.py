import random

import variables as vs
from conftest import PLATFORM
from element_wrapper import ElementWrapper


class MainCurrency:
    CURRENCY_PICKER = "Select currency Picker"
    if PLATFORM == "Android":
        SELECTED_CURRENCY = '//android.view.ViewGroup[@content-desc="Main Currency"]/android.view.ViewGroup/android.widget.TextView[2]'
    else:
        SELECTED_CURRENCY = 'label == "Main Currency"'

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def set_currency(self, currency):
        """ Selecting main currency of user
        :param currency: str
        """

        if currency == "random":
            currency = random.choice(vs.accessible_currencies)

        self.ew.wait_and_tap_element(f"Currency {currency}", 10)
        self.ew.wait_till_element_is_not_visible(self.CURRENCY_PICKER, 10)

    def get_currency(self):
        """ Getting selected main currency
        :return: str
        """
        self.ew.wait_till_element_is_visible(self.SELECTED_CURRENCY, 10)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_CURRENCY)
        else:
            return self.ew.get_attribute(self.SELECTED_CURRENCY, "name")
