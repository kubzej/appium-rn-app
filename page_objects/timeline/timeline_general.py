from element_wrapper import ElementWrapper


class TimelineGeneral:
    ADD_TRANSACTION_BUTTON = "Add Transaction Button"
    OVERVIEW_BUTTON = "Overview Button"
    NAVIGATION_TIMELINE = "Navigation Timeline"
    SCHEDULED = "Scheduled"
    SCHEDULED_SCREEN = "Scheduled Screen"
    TRANSACTION_CATEGORY_PICKER = "Transaction Category Picker"
    TRANSACTION_SECTION = "Transaction Section"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def go_to_timeline(self):
        """Opens Timeline section"""
        self.ew.wait_and_tap_element(self.NAVIGATION_TIMELINE, 30)
        self.ew.wait_till_element_is_visible(self.ADD_TRANSACTION_BUTTON, 10)

    def open_transaction_create_screen(self):
        """Opens transaction create screen"""
        self.ew.wait_and_tap_element(self.NAVIGATION_TIMELINE, 30)
        self.ew.wait_and_tap_element(self.ADD_TRANSACTION_BUTTON, 30)
        self.ew.wait_till_element_is_visible(self.TRANSACTION_CATEGORY_PICKER, 15)

    def open_scheduled_section(self):
        """Opens Scheduled section"""
        self.ew.wait_and_tap_element(self.SCHEDULED, 30)
        self.ew.wait_till_element_is_visible(self.SCHEDULED_SCREEN, 5)
