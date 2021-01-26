from element_wrapper import ElementWrapper
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail


class TransactionActions:

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
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
