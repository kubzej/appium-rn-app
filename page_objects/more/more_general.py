from element_wrapper import ElementWrapper


class MoreGeneral:

    NAVIGATION_MORE = "Navigation More"
    MORE_HEADER = "More Header"
    LOGOUT_BUTTON = "Logout Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def go_to_more_section(self):
        self.ew.wait_and_tap_element(self.NAVIGATION_MORE, 30)
        self.ew.wait_till_element_is_visible(self.MORE_HEADER, 10)