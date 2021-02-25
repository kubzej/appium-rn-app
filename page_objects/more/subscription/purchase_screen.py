from element_wrapper import ElementWrapper


class PurchaseScreen:
    SUBSCRIPTION_HEADER = "Subscription Header"
    BACK_BUTTON = "Back Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
