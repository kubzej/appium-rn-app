from element_wrapper import ElementWrapper

class WalletOverview:

    BACK_BUTTON = "Back Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)