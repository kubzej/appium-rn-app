from element_wrapper import ElementWrapper


class BankSearchScreen():

    SEARCH_INPUT = "Search Input"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def search_bank_by_search_box(self, bank):
        if bank == "random":
            bank = "Fake Bank Simple"

        self.ew.get_element(self.SEARCH_INPUT).send_keys(bank)
