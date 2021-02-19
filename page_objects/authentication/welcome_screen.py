from selenium.common.exceptions import NoSuchElementException

from conftest import PLATFORM
from element_wrapper import ElementWrapper


class WelcomeScreen:

    WELCOME_SCREEN = "Welcome Screen"
    SIGN_UP_WITH_EMAIL_BUTTON = "Sign Up With Email"
    LOGIN_WITH_EMAIL_BUTTON = "Login With Email"
    SIGN_IN_WITH_GOOGLE_BUTTON = "Sign In With Google"
    SIGN_IN_WITH_FACEBOOK = "Sign In With Facebook"
    SIGN_IN_WITH_APPLE = "Sign In With Apple"
    NOTIFICATIONS_ALERT = '“Spendee” Would Like to Send You Notifications'
    ALLOW_NOTIFICATIONS_BUTTON = "Allow"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def open_sign_up_email_screen(self):
        self.ew.wait_and_tap_element(self.SIGN_UP_WITH_EMAIL_BUTTON, 20)

    def open_login_by_email_screen(self):
        self.ew.wait_and_tap_element(self.LOGIN_WITH_EMAIL_BUTTON, 30)

    def skip_notifications_alert(self):
        try:
            self.ew.wait_till_element_is_visible(self.WELCOME_SCREEN, 1)
        except NoSuchElementException:
            pass
        if PLATFORM == "iOS" and self.ew.is_element_present(self.NOTIFICATIONS_ALERT):
            self.ew.tap_element(self.ALLOW_NOTIFICATIONS_BUTTON)