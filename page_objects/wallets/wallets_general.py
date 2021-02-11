from element_wrapper import ElementWrapper


class WalletsGeneral:

    NAVIGATION_WALLETS = "Navigation Wallets"
    WALLETS_ANIMATED_HEADER = "Wallets Animated Header"
    ADD_WALLET_BUTTON = "Add Wallet Button"
    CONNECT_BANK_BUTTON = "Connect Bank Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def go_to_wallets(self):
        self.ew.wait_and_tap_element(self.NAVIGATION_WALLETS, 30)
        self.ew.wait_till_element_is_visible(self.WALLETS_ANIMATED_HEADER, 30)
