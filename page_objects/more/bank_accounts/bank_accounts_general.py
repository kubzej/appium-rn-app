from conftest import PLATFORM
from element_wrapper import ElementWrapper


class BankAccountsGeneral():
    CONNECT_BANK_ACCOUNT_BUTTON = "Connect Bank Account Button"
    BACK_BUTTON = "Back Button"

    if PLATFORM == "Android":
        BANK_ITEM = "Bank Item"
        BANK_ITEM_NAME = '//android.view.ViewGroup[@content-desc="Bank Item"]/android.widget.TextView'
    else:
        BANK_ITEM = '**/XCUIElementTypeOther[`label == "Bank Item"`][3]'

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def open_bank_account(self):
        """Opens bank account settings"""
        self.ew.wait_and_tap_element(self.BANK_ITEM, 15)
