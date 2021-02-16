from element_wrapper import ElementWrapper
from page_objects.more.bank_accounts.bank_accounts_general import BankAccountsGeneral
from page_objects.more.bank_accounts.bank_search_screen import BankSearchScreen


class BankAccountsActions():

    def __init__(self, driver):
        self.driver = driver
        self.bank_accounts_general = BankAccountsGeneral(self.driver)
        self.bank_search_screen = BankSearchScreen(self.driver)
        self.ew = ElementWrapper(self.driver)

    def connect_bank_account(self, bank):
        self.ew.wait_and_tap_element(self.bank_accounts_general.CONNECT_BANK_ACCOUNT_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.bank_search_screen.SEARCH_INPUT, 30)
        self.bank_search_screen.search_bank_by_search_box(bank)
