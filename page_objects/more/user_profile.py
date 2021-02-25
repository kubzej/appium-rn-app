from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.more.more_general import MoreGeneral


class UserProfile:
    # More About You
    CONTINUE_BUTTON = "Continue Button"
    MORE_ABOUT_YOU_HEADER = "More About You Header"

    # Profile
    if PLATFORM == "Android":
        USER_PROFILE = "User Profile"
    else:
        USER_PROFILE = 'label == "User Profile"'
    BACK_BUTTON = "Back Button"

    if PLATFORM == "Android":
        FIRST_NAME = "First Name Input"
        LAST_NAME = "Last Name Input"
    else:
        FIRST_NAME = "(//XCUIElementTypeTextField[@name='RNE__Input__text-input'])[1]"
        LAST_NAME = "(//XCUIElementTypeTextField[@name='RNE__Input__text-input'])[2]"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.more_general = MoreGeneral(self.driver)

    def set_first_name(self, first_name):
        self.ew.wait_till_element_is_visible(self.FIRST_NAME, 5)
        self.ew.get_element(self.FIRST_NAME).send_keys(first_name)

    def set_last_name(self, last_name):
        self.ew.wait_till_element_is_visible(self.LAST_NAME, 5)
        self.ew.get_element(self.LAST_NAME).send_keys(last_name)

    def clear_first_name(self):
        self.ew.get_element(self.FIRST_NAME).clear()

    def clear_last_name(self):
        self.ew.get_element(self.LAST_NAME).clear()

    def get_full_name(self):
        first_name = self.ew.get_text_of_element(self.FIRST_NAME)
        last_name = self.ew.get_text_of_element(self.LAST_NAME)
        return f"{first_name} {last_name}"

    def save_user_profile(self):
        self.ew.tap_element(self.BACK_BUTTON)
        self.ew.wait_till_element_is_visible(self.more_general.MORE_HEADER, 10)
