from element_wrapper import ElementWrapper
from conftest import PLATFORM


class BankSearchScreen():

    SEARCH_INPUT = "Search Input"
    if PLATFORM == "Android":
        BANK_ITEM = "Bank Item"
    else:
        BANK_ITEM = 'label == "Bank Item"'

    BACK_BUTTON = "Back Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def search_bank_by_search_box(self, bank):
        if bank == "random":
            bank = "Fake Bank Simple"

        self.ew.get_element(self.SEARCH_INPUT).send_keys(bank)
        if PLATFORM == "Android":
            self.ew.wait_till_element_is_visible(bank, 15)
        else:
            self.ew.wait_till_element_is_visible(f'label == "Bank Item" AND name == "{bank}"', 15)
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        self.ew.wait_and_tap_element(self.BANK_ITEM, 15)


