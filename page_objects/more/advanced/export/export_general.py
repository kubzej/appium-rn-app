from element_wrapper import ElementWrapper


class ExportGeneral:

    EXPORT_HEADER = "Export Header"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)