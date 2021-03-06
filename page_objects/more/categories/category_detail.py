import random
import string

import validator as vr
import variables as vs
from conftest import PLATFORM
from element_wrapper import ElementWrapper


class CategoryDetail:
    CATEGORY_HEADER = "Category Header"
    SELECTED_ATTRIBUTES = '//android.view.ViewGroup[@content-desc="Category Icon"]/android.view.ViewGroup'
    SAVE_CATEGORY_BUTTON = "Save Category Button"
    TRASH_ICON = "Trash Icon"
    DELETE_BUTTON = "Delete"

    # NAME
    NAME_INPUT = "Name Input"
    SELECTED_NAME_IOS = '**/XCUIElementTypeTextField[`label == "Name Input"`]'

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def set_name(self, name):
        """ Insets name into name input
        :param name: str
        """
        if name == "random":
            name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(0, 8)])

        self.ew.wait_till_element_is_visible(self.NAME_INPUT, 5)
        self.ew.get_element(self.NAME_INPUT).send_keys(name)

        vr.validate_input_against_output(name, self.get_name())

    def get_name(self):
        """ Gets name from name input
        :return: str
        """
        self.ew.wait_till_element_is_visible(self.NAME_INPUT, 5)

        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.NAME_INPUT)
        else:
            return self.ew.get_text_of_element(self.SELECTED_NAME_IOS)

    def set_color(self, color):
        """ Selects color from visible colors
        :param color: str
        """
        if color == "random":
            color = random.choice(vs.accessible_colors)

        self.ew.wait_and_tap_element(color, 5)

        vr.validate_input_against_output(color, self.get_color())

    def get_color(self):
        """ Gets #rgb of selected color
        :return: str
        """
        self.ew.wait_till_element_is_visible(self.SELECTED_ATTRIBUTES, 5)
        name, color, image = self.ew.get_attribute(self.SELECTED_ATTRIBUTES, 'content-desc').split('/')
        return color

    def set_image(self, image):
        """ Sets image from visible images
        :param image: str or int
        """
        if image == "random":
            image = random.randrange(1, 20)

        self.ew.wait_and_tap_element(image, 5)

        vr.validate_input_against_output(str(image), self.get_image())

    def get_image(self):
        """ Gets id of selected image
        :return: str
        """
        self.ew.wait_till_element_is_visible(self.SELECTED_ATTRIBUTES, 5)
        name, color, image = self.ew.get_attribute(self.SELECTED_ATTRIBUTES, 'content-desc').split('/')
        return image
