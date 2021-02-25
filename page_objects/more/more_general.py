from conftest import PLATFORM
from element_wrapper import ElementWrapper


class MoreGeneral:
    NAVIGATION_MORE = "Navigation More"
    MORE_HEADER = "More Header"
    LOGOUT_BUTTON = "Logout Button"

    # PROFILE
    if PLATFORM == "Android":
        USER_PROFILE = "User Profile"
    else:
        USER_PROFILE = 'label == "User Profile"'
    PROFILE_HEADER = "Profile Header"
    USER_NAME_ANDROID = "//android.view.ViewGroup[@content-desc='User Profile']/android.view.ViewGroup/android.widget.TextView[1]"

    # CATEGORIES
    if PLATFORM == "Android":
        CATEGORIES = "Categories"
        CATEGORIES_HEADER = "Categories Header"
    else:
        CATEGORIES = 'label == "Categories"'
        CATEGORIES_HEADER = 'label == "Categories Header"'

    # BANK ACCOUNTS
    BANK_ACCOUNTS = "Bank Accounts"
    BANK_ACCOUNTS_HEADER = "Bank Accounts Header"

    # ADVANCED
    ADVANCED = "Advanced"
    ADVANCED_HEADER = "Advanced Header"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def go_to_more_section(self):
        """Opens More section"""
        self.ew.wait_and_tap_element(self.NAVIGATION_MORE, 60)
        self.ew.wait_till_element_is_visible(self.MORE_HEADER, 10)

    def go_to_user_profile(self):
        """Opens User Profile section"""
        self.ew.wait_and_tap_element(self.USER_PROFILE, 10)
        self.ew.wait_till_element_is_visible(self.PROFILE_HEADER, 10)

    def get_full_name_on_more_section(self):
        """ Gets full name visible inside More section
        :return: str
        """
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.USER_NAME_ANDROID)
        else:
            return self.ew.get_attribute(self.USER_PROFILE, "name")

    def go_to_categories(self):
        """Opens Categories section"""
        self.ew.wait_and_tap_element(self.CATEGORIES, 10)
        self.ew.wait_till_element_is_visible(self.CATEGORIES_HEADER, 10)

    def go_to_bank_accounts(self):
        """Opens Bank Accounts section"""
        self.ew.wait_and_tap_element(self.BANK_ACCOUNTS, 10)
        self.ew.wait_till_element_is_visible(self.BANK_ACCOUNTS_HEADER, 10)

    def go_to_advanced(self):
        """Opens Advanced section"""
        self.ew.wait_and_tap_element(self.ADVANCED, 10)
        self.ew.wait_till_element_is_visible(self.ADVANCED_HEADER, 10)
