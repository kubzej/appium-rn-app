from element_wrapper import ElementWrapper
from page_objects.more.advanced.export.export_general import ExportGeneral


class AdvancedGeneral:
    ADVANCED_HEADER = "Advanced Header"
    EXPORT = "Export"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.export_general = ExportGeneral(self.driver)

    def go_to_export(self):
        self.ew.wait_and_tap_element(self.EXPORT, 10)
        self.ew.wait_till_element_is_visible(self.export_general.EXPORT_HEADER, 10)
