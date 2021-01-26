from element_wrapper import ElementWrapper


class EmailPassword:

    EMAIL_INPUT = "Email Input"
    PASSWORD_INPUT = "Password Input"
    LOGIN_BUTTON = "Login Button"
    SIGN_UP_BUTTON = "Sign Up Button"
    ERROR_DIALOG = "Error Dialog"
    VALIDATION_ERROR_WARNING = "Validation Error Warning"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def set_email(self, email):
        self.ew.wait_till_element_is_visible(self.EMAIL_INPUT, 5)
        self.ew.get_element(self.EMAIL_INPUT).send_keys(email)

    def set_password(self, password):
        self.ew.wait_till_element_is_visible(self.PASSWORD_INPUT, 5)
        self.ew.get_element(self.PASSWORD_INPUT).send_keys(password)