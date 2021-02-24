import time

from selenium.common.exceptions import NoSuchElementException

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.authentication.email_password import EmailPassword
from page_objects.authentication.marketing_dialog import MarketingDialog
from page_objects.authentication.welcome_screen import WelcomeScreen
from page_objects.more.more_general import MoreGeneral
from page_objects.more.user_profile import UserProfile
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.authentication.facebook import Facebook
from page_objects.authentication.google import Google


class AuthenticationActions:

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.email_password = EmailPassword(self.driver)
        self.facebook = Facebook(self.driver)
        self.google = Google(self.driver)
        self.marketing_dialog = MarketingDialog(self.driver)
        self.more_general = MoreGeneral(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.user_profile = UserProfile(self.driver)
        self.welcome_screen = WelcomeScreen(self.driver)

    def register_by_email(self, email, password):
        self.welcome_screen.open_sign_up_email_screen()
        self.email_password.set_email(email)
        self.email_password.set_password(password)
        self.ew.tap_element(self.email_password.SIGN_UP_BUTTON)
        time.sleep(0.5)
        if PLATFORM == "iOS":
            self.marketing_dialog.agree_with_ios_notifications()

    def login_by_facebook(self, email, password):
        self.welcome_screen.open_login_by_facebook()
        self.ew.wait_till_element_is_visible(self.facebook.FACEBOOK_HEADER, 30)
        if self.ew.is_element_present(self.facebook.COOKIES_ACCEPT_BUTTON):
            self.ew.tap_element(self.facebook.COOKIES_ACCEPT_BUTTON)
        self.ew.get_element(self.facebook.EMAIL_TEXT_BOX).send_keys(email)
        self.ew.get_element(self.facebook.PASSWORD_TEXT_BOX).send_keys(password)
        self.ew.wait_and_tap_element(self.facebook.LOGIN_BUTTON, 10)
        self.ew.wait_and_tap_element(self.facebook.CONTINUE_BUTTON, 20)
        if PLATFORM == "iOS":
            self.marketing_dialog.agree_with_ios_notifications()

    def login_by_email(self, email, password):
        self.welcome_screen.open_login_by_email_screen()
        self.email_password.set_email(email)
        self.email_password.set_password(password)
        self.ew.tap_element(self.email_password.LOGIN_BUTTON)
        if PLATFORM == "iOS":
            self.marketing_dialog.agree_with_ios_notifications()

    def login_by_google(self):
        self.welcome_screen.open_login_by_google()
        self.ew.wait_and_tap_element(self.google.EMAIL_TO_SELECT, 20)

    def logout(self):
        self.more_general.go_to_more_section()
        self.ew.swipe_if_element_not_present(self.more_general.LOGOUT_BUTTON)
        self.ew.tap_element(self.more_general.LOGOUT_BUTTON)



