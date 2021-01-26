from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.more.more_general import MoreGeneral


class UserProfile:

    # More About You
    CONTINUE_BUTTON = "Continue Button"
    MORE_ABOUT_YOU_HEADER = "More About You Header"

    # Profile
    USER_PROFILE = "User Profile"
    PROFILE_HEADER = "Profile Header"
    BACK_BUTTON = "Back Button"

    # More section
    USER_NAME_ANDROID = "//android.view.ViewGroup[@content-desc='User Profile']/android.widget.TextView[1]"

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


    def go_to_user_profile(self):
        self.ew.wait_and_tap_element(self.USER_PROFILE, 10)
        self.ew.wait_till_element_is_visible(self.PROFILE_HEADER, 10)

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

    def get_full_name_on_more_section(self):
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.USER_NAME_ANDROID)
        else:
            return self.ew.get_attribute(self.USER_PROFILE, "name")

    def save_user_profile(self):
        self.ew.tap_element(self.BACK_BUTTON)
        self.ew.wait_till_element_is_visible(self.more_general.MORE_HEADER, 10)


