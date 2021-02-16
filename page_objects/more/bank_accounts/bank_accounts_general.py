from element_wrapper import ElementWrapper


class BankAccountsGeneral():

    CONNECT_BANK_ACCOUNT_BUTTON = "Connect Bank Account Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)