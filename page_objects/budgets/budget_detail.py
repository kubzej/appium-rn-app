from element_wrapper import ElementWrapper
from conftest import PLATFORM
import string
import random
import time
import validator as vr
import variables as vs


class BudgetDetail():

    # OTHER
    BUDGET_HEADER = "Budget Header"

    # NAME
    NAME_INPUT = "Name Input"
    SELECTED_NAME_IOS = '**/XCUIElementTypeTextField[`label == "Name Input"`]'

    # AMOUNT
    if PLATFORM == "Android":
        AMOUNT_INPUT = "Amount Input"
    else:
        AMOUNT_INPUT = '**/XCUIElementTypeOther[`label == "Amount Input"`][2]'
    SELECTED_AMOUNT = "Currency Input"

    # KEYBOARD
    KEYBOARD = {"0": "Numpad 0", "1": "Numpad 1", "2": "Numpad 2", "3": "Numpad 3", "4": "Numpad 4", "5": "Numpad 5",
                "6": "Numpad 6", "7": "Numpad 7", "8": "Numpad 8", "9": "Numpad 9",
                ".": "Numpad Decimal Point", ",": "Numpad Decimal Point"}
    NUMPAD_BACKDROP = "Numpad Backdrop"
    NUMPAD_CLEAR = "Numpad Clear"

    # CURRENCY
    CURRENCY = "Currency"

    if PLATFORM == "Android":
        SELECTED_CURRENCY = '//android.view.ViewGroup[@content-desc="Currency"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText'
        CURRENCY_PICKER = "Select currency Picker"
    else:
        SELECTED_CURRENCY = '**/XCUIElementTypeOther[`label == "Currency"`][1]'
        CURRENCY_PICKER = 'label == "Select currency"'

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def set_name(self, name):
        if name == "random":
            name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(0, 8)])

        self.ew.wait_till_element_is_visible(self.NAME_INPUT, 5)
        self.ew.get_element(self.NAME_INPUT).send_keys(name)

        vr.validate_input_against_output(name, self.get_name())

    def get_name(self):
        self.ew.wait_till_element_is_visible(self.NAME_INPUT, 5)

        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.NAME_INPUT)
        else:
            return self.ew.get_text_of_element(self.SELECTED_NAME_IOS)

    def set_amount(self, amount):
        if amount == "random":
            amount = str(random.randint(1, 99))

        self.ew.wait_and_tap_element(self.AMOUNT_INPUT, 5)
        self.ew.wait_till_element_is_visible(self.KEYBOARD["1"], 10)
        amount_list = list(amount)
        for i in amount_list:
            self.ew.wait_and_tap_element(self.KEYBOARD[i], 5)
        self.ew.wait_and_tap_element(self.NUMPAD_BACKDROP, 5)

        vr.validate_input_against_output(amount, self.get_amount())

    def get_amount(self):
        self.ew.wait_till_element_is_visible(self.AMOUNT_INPUT, 5)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_AMOUNT)
        else:
            return self.ew.get_attribute(self.AMOUNT_INPUT, "name")

    def set_currency(self, currency):
        if currency == "random":
            currency = random.choice(vs.accessible_currencies)

        self.ew.wait_and_tap_element(self.CURRENCY, 5)
        self.ew.wait_till_element_is_visible(self.CURRENCY_PICKER, 5)
        self.ew.wait_and_tap_element(f"Currency {currency}", 10)

        self.ew.wait_till_element_is_not_visible(self.CURRENCY_PICKER, 10)
        vr.validate_input_against_output(currency, self.get_currency())

    def get_currency(self):
        self.ew.wait_till_element_is_visible(self.CURRENCY, 5)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_CURRENCY)
        else:
            return self.ew.get_attribute(self.SELECTED_CURRENCY, "name")

    def set_wallets(self, wallets):
        # random - vyberu náhodný počet
        # all = vyberu všechny
        # none = žádná
        # podle jména
        # podle čísla

        self.ew.wait_and_tap_element("Wallets", 5)