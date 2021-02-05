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

    # WALLETS
    if PLATFORM == "Android":
        WALLET_ITEM = '//android.view.ViewGroup[@content-desc="Select Wallets Picker"]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup'
        WALLETS = "Wallets"
    else:
        WALLET_ITEM = "Wallet Item"
        WALLETS = 'label == "Wallets"'
    WALLET_PICKER = "Select Wallets Picker"
    SELECTED_WALLETS_ANDROID = '//android.view.ViewGroup[@content-desc="Wallets"]/android.view.ViewGroup/android.widget.TextView[2]'

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

        self.ew.wait_and_tap_element(self.WALLETS, 5)
        self.ew.wait_till_element_is_visible(self.WALLET_PICKER, 5)

        all_visible_wallets = self.count_wallets()[0]
        selected_wallets = self.count_wallets()[1]
        non_selected_wallets = self.count_wallets()[2]
        total_wallets = len(all_visible_wallets)
        total_selected_wallets = len(selected_wallets)
        total_non_selected_wallets = len(non_selected_wallets)

        if wallets == "random":
            wallets_to_select = random.sample(all_visible_wallets, random.randrange(0, len(all_visible_wallets)))
            for i in wallets_to_select:
                if PLATFORM == "Android":
                    self.ew.tap_element(i)
                else:
                    self.ew.tap_element(f'label == "{i}"')
        elif wallets == "all_selected":
            if total_wallets != total_selected_wallets:
                for i in non_selected_wallets:
                    if PLATFORM == "Android":
                        self.ew.tap_element(i)
                    else:
                        self.ew.tap_element(f'label == "{i}"')
        elif wallets == "none_selected":
            if total_wallets != total_non_selected_wallets:
                for i in selected_wallets:
                    if PLATFORM == "Android":
                        self.ew.tap_element(i)
                    else:
                        self.ew.tap_element(f'label == "{i}"')
        elif isinstance(wallets, int):
            x = 0
            actual_selected_wallets = self.count_wallets()[1]
            for i in all_visible_wallets:
                x = x + 1
                if x <= wallets and len(actual_selected_wallets) > 1:
                    if PLATFORM == "Android":
                        self.ew.tap_element(i)
                    else:
                        self.ew.tap_element(f'label == "{i}"')
                    actual_selected_wallets = self.count_wallets()[1]

        selected_wallets = self.count_wallets()[1]
        total_wallets = len(self.count_wallets()[0])
        total_selected_wallets = len(selected_wallets)

        if total_wallets == total_selected_wallets:
            v_input = "All Wallets"
        elif total_selected_wallets == 1:
            v_input = selected_wallets[0].split('-')[0]
        else:
            v_input = str(total_selected_wallets)

        self.ew.tap_element('Backdrop')
        vr.validate_input_against_output(v_input, self.get_wallets())

    def count_wallets(self):
        if PLATFORM == "Android":
            all_visible_wallets = self.ew.get_attributes(self.WALLET_ITEM, "content-desc")
        else:
            all_visible_wallets = self.ew.get_attributes(self.WALLET_ITEM, "label")

        selected_wallets = []
        non_selected_wallets = []
        for i in all_visible_wallets:
            if i.endswith('true'):
                selected_wallets.append(i)
            else:
                non_selected_wallets.append(i)
        return (all_visible_wallets, selected_wallets, non_selected_wallets)

    def get_wallets(self):
        self.ew.wait_till_element_is_visible(self.WALLETS, 5)

        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_WALLETS_ANDROID)
        else:
            return self.ew.get_attribute(self.WALLETS, "name")
