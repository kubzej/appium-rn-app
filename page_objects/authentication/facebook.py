from conftest import PLATFORM
from element_wrapper import ElementWrapper


class Facebook():
    if PLATFORM == "Android":
        FACEBOOK_HEADER = "facebook"
        COOKIES_ACCEPT_BUTTON = "Accept All Accept All"
        EMAIL_TEXT_BOX = '//android.webkit.WebView[@content-desc="Log into Facebook | Facebook"]/android.view.View/' \
                         'android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View[2]/' \
                         'android.view.View[1]/android.view.View[2]/android.view.View[1]/android.widget.EditText'
        PASSWORD_TEXT_BOX = '//android.webkit.WebView[@content-desc="Log into Facebook | Facebook"]/android.view.View/' \
                            'android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View[2]/' \
                            'android.view.View[1]/android.view.View[2]/android.widget.EditText'
        LOGIN_BUTTON = 'Log In '
        CONTINUE_BUTTON = '(//android.widget.Button)[2]'
    else:
        FACEBOOK_HEADER = '//XCUIElementTypeOther[@name="Facebook"]'
        COOKIES_ACCEPT_BUTTON = '//XCUIElementTypeOther[@name="Accept All"]'
        EMAIL_TEXT_BOX = '//XCUIElementTypeOther[@name="main"]/XCUIElementTypeTextField'
        PASSWORD_TEXT_BOX = '//XCUIElementTypeOther[@name="main"]/XCUIElementTypeSecureTextField'
        LOGIN_BUTTON = '//XCUIElementTypeButton[@name="Log In"]'
        CONTINUE_BUTTON = '(//XCUIElementTypeButton)[5]'

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
