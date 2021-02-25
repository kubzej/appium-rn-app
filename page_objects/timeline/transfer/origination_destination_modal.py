from element_wrapper import ElementWrapper
from page_objects.timeline.transaction.transaction_detail import TransactionDetail


class TransferOriginationModal():
    ORIGINATION_MODAL = "Transfer Origination"
    DESTINATION_MODAL = "Transfer Destination"
    CONFIRM_BUTTON = "Confirm Button"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)

    def create_as_new_transaction(self):
        self.ew.tap_element(self.CONFIRM_BUTTON)

    def is_origination_modal_present(self):
        self.ew.wait_till_element_is_not_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 10)
        if self.ew.is_element_present(self.ORIGINATION_MODAL):
            return True
        else:
            return False


class TransferDestinationModal(TransferOriginationModal):

    def is_destination_modal_present(self):
        self.ew.wait_till_element_is_not_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 10)
        if self.ew.is_element_present(self.DESTINATION_MODAL):
            return True
        else:
            return False
