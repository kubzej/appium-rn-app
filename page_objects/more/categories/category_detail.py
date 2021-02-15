from element_wrapper import ElementWrapper


class CategoryDetail:

    CATEGORY_HEADER = "Category Header"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)