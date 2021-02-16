from element_wrapper import ElementWrapper
from page_objects.more.bank_accounts.bank_accounts_general import BankAccountsGeneral
from page_objects.more.bank_accounts.bank_search_screen import BankSearchScreen
import secrets as s
from conftest import PLATFORM


class BankAccountsActions():

    if PLATFORM == "Android":
        LOGIN_INPUT = '//android.webkit.WebView[@content-desc="Spendee"]/android.view.View[2]/android.view.View[2]/android.widget.EditText'
        PASSWORD_INPUT = '//android.webkit.WebView[@content-desc="Spendee"]/android.view.View[2]/android.view.View[3]/android.widget.EditText'
    else:
        LOGIN_INPUT = '//XCUIElementTypeOther[@name="Spendee"]/XCUIElementTypeTextField'
        PASSWORD_INPUT = '//XCUIElementTypeOther[@name="Spendee"]/XCUIElementTypeSecureTextField'

    CONTINUE_BUTTON = "Continue"

    def __init__(self, driver):
        self.driver = driver
        self.bank_accounts_general = BankAccountsGeneral(self.driver)
        self.bank_search_screen = BankSearchScreen(self.driver)
        self.ew = ElementWrapper(self.driver)

    def connect_bank_account(self, bank):
        self.ew.wait_and_tap_element(self.bank_accounts_general.CONNECT_BANK_ACCOUNT_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.bank_search_screen.SEARCH_INPUT, 30)
        self.bank_search_screen.search_bank_by_search_box(bank)
        self.ew.wait_till_element_is_visible(self.LOGIN_INPUT, 15)
        self.ew.get_element(self.LOGIN_INPUT).send_keys(s.login_fake_bank)
        self.ew.get_element(self.PASSWORD_INPUT).send_keys(s.password_fake_bank)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        self.ew.wait_and_tap_element(self.CONTINUE_BUTTON, 5)
        self.ew.wait_till_element_is_visible(self.bank_search_screen.SEARCH_INPUT, 120)
        self.ew.tap_element(self.bank_search_screen.BACK_BUTTON)
        self.ew.wait_till_element_is_visible(self.bank_accounts_general.CONNECT_BANK_ACCOUNT_BUTTON, 10)