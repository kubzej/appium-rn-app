from element_wrapper import ElementWrapper


class EmailPassword:
    EMAIL_INPUT = "Email Input"
    PASSWORD_INPUT = "Password Input"
    EXISTING_EMAIL_DIALOG = "Email Already In Use Dialog"
    LOGIN_BUTTON = "Login Button"
    SIGN_UP_BUTTON = "Sign Up Button"
    INVALID_CREDENTIALS_DIALOG = "Invalid Credentials Dialog"
    VALIDATION_ERROR_WARNING = "Validation Error Warning"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def set_email(self, email):
        """ Inserts email of user into email input
        :param email: str
        """
        self.ew.wait_till_element_is_visible(self.EMAIL_INPUT, 5)
        self.ew.get_element(self.EMAIL_INPUT).send_keys(email)

    def set_password(self, password):
        """ Inserts password of user into password input
        :param password: str
        """
        self.ew.wait_till_element_is_visible(self.PASSWORD_INPUT, 5)
        self.ew.get_element(self.PASSWORD_INPUT).send_keys(password)
