from element_wrapper import ElementWrapper


class WalletDetail:

    # OTHER
    WALLET_HEADER = "Wallet Header"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)