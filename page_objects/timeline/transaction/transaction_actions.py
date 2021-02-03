from element_wrapper import ElementWrapper
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from page_objects.timeline.transfer.origination_destination_modal import TransferDestinationModal
from selenium.common.exceptions import NoSuchElementException

class TransactionActions:

    EXISTING_TRANSACTION = "Existing Item: regular"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.transfer_destination_modal = TransferDestinationModal(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)

    def create_transaction(self, transaction_type, category, amount, currency, wallet, start_date, note, label, photo,
                           reminder):
        self.timeline_general.open_transaction_create_screen()
        if transaction_type is not None:
            self.transaction_detail.set_type_of_transaction(transaction_type)
        self.transaction_detail.set_category(category)
        self.transaction_detail.set_amount(amount)
        if currency is not None:
            self.transaction_detail.set_currency(currency)
        if wallet is not None:
            self.transaction_detail.set_wallet(wallet, "transaction")
        if start_date is not None:
            self.transaction_detail.set_start_date(start_date)
        if note is not None:
            self.transaction_detail.set_note(note)
        if label is not None:
            self.transaction_detail.set_label(label)
        if photo is not None:
            self.transaction_detail.set_photo()
        if reminder is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.REMINDER)
            self.transaction_detail.set_reminder(reminder)
        self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)

    def save_transaction(self):
        self.ew.wait_and_tap_element(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
        if self.transfer_destination_modal.is_destination_modal_present() or self.transfer_destination_modal.is_origination_modal_present():
            self.transfer_destination_modal.create_as_new_transaction()

    def open_transaction(self):

        self.ew.wait_till_element_is_visible(self.timeline_general.OVERVIEW_BUTTON, 30)
        self.timeline_general.go_to_timeline()
        if self.ew.is_element_present(self.EXISTING_TRANSACTION) is False:
            self.create_transaction(transaction_type="random", category="random", amount="random", currency=None, wallet=None, start_date=None, note=None, label=None, photo=None, reminder=None)
            self.save_transaction()
            self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)
        self.ew.wait_and_tap_element(self.EXISTING_TRANSACTION, 15)
        self.ew.wait_till_element_is_visible(self.transaction_detail.TRANSACTION_HEADER_TITLE, 15)

    def edit_transaction(self, transaction_type, category, amount, wallet, start_date, note, label, photo, reminder):
        if transaction_type is not None:
            self.ew.tap_element(self.transaction_detail.CATEGORY_ICON)
            if transaction_type == "transfer":
                self.transaction_detail.set_type_to_transfer()
            else:
                self.transaction_detail.set_type_of_transaction(transaction_type)
                self.transaction_detail.set_category("random")
        if category is not None:
            self.ew.tap_element(self.transaction_detail.CATEGORY_ICON)
            self.transaction_detail.set_category(category)
        if amount is not None:
            self.ew.tap_element(self.transaction_detail.AMOUNT_INPUT)
            self.ew.wait_till_element_is_visible(self.transaction_detail.NUMPAD_CLEAR, 10)
            for i in range(6):
                self.ew.tap_element(self.transaction_detail.NUMPAD_CLEAR)
            self.transaction_detail.set_amount(amount)
        if wallet is not None:
            self.transaction_detail.set_wallet(wallet, "transaction")
        if start_date is not None:
            self.transaction_detail.set_start_date(start_date)
        if note is not None:
            try:
                self.ew.get_element(self.transaction_detail.EXISTING_NOTE).clear()
            except NoSuchElementException:
                pass
            self.transaction_detail.set_note(note)
        if label is not None:
            self.transaction_detail.set_label(label)
        if photo is not None:
            self.transaction_detail.set_photo()
        if reminder is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.REMINDER)
            self.transaction_detail.set_reminder(reminder)
        self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)

    def delete_transaction(self):
        self.ew.wait_and_tap_element(self.transaction_detail.TRASH_ICON, 10)
        self.ew.wait_and_tap_element(self.transaction_detail.DELETE_BUTTON, 10)