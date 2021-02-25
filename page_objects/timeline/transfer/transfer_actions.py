from selenium.common.exceptions import NoSuchElementException

from element_wrapper import ElementWrapper
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_actions import TransactionActions
from page_objects.timeline.transaction.transaction_detail import TransactionDetail


class TransferActions():
    EXISTING_TRANSFER = "Existing Item: transfer-undefined"
    EXISTING_TRANSFER_TEMPLATES = ["Existing Item: transfer-every day", "Existing Item: transfer-every 2 days",
                                   "Existing Item: transfer-every working day", "Existing Item: transfer-every week",
                                   "Existing Item: transfer-every 2 weeks", "Existing Item: transfer-every 4 weeks",
                                   "Existing Item: transfer-every month", "Existing Item: transfer-every 2 months",
                                   "Existing Item: transfer-every 3 months", "Existing Item: transfer-every 6 months",
                                   "Existing Item: transfer-every year"]

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transaction_actions = TransactionActions(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)

    def create_transfer(self, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date,
                        reminder):
        self.timeline_general.open_transaction_create_screen()
        self.transaction_detail.set_type_to_transfer()
        self.transaction_detail.set_amount(amount)
        if outgoing_wallet is not None:
            self.transaction_detail.set_wallet(outgoing_wallet, "transfer_outgoing")
        if incoming_wallet is not None:
            self.transaction_detail.set_wallet(incoming_wallet, "transfer_incoming")
        if start_date is not None:
            self.transaction_detail.set_start_date(start_date)
        if note is not None:
            self.transaction_detail.set_note(note)
        if recurrence is not None:
            self.transaction_detail.set_recurrence(recurrence)
        if end_date is not None:
            self.transaction_detail.set_end_date(end_date)
        if reminder is not None:
            self.transaction_detail.set_reminder(reminder)

    def open_transfer(self):

        self.timeline_general.go_to_timeline()
        self.ew.wait_till_element_is_visible(self.timeline_general.ADD_TRANSACTION_BUTTON, 30)
        print(self.ew.is_element_present(self.EXISTING_TRANSFER))
        if self.ew.is_element_present(self.EXISTING_TRANSFER) is False:
            self.create_transfer(amount="random", outgoing_wallet=None, incoming_wallet=None, start_date=None,
                                 note=None, recurrence=None, end_date=None, reminder=None)
            self.transaction_actions.save_transaction()
            self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)
        self.ew.wait_and_tap_element(self.EXISTING_TRANSFER, 15)
        self.ew.wait_till_element_is_visible(self.transaction_detail.TRANSACTION_HEADER_TITLE, 15)

    def open_transfer_template(self):
        self.ew.wait_till_element_is_visible(self.timeline_general.TRANSACTION_SECTION, 60)
        if self.ew.is_element_present(self.timeline_general.SCHEDULED) is True:
            self.timeline_general.open_scheduled_section()
            for i in self.EXISTING_TRANSFER_TEMPLATES:
                if self.ew.is_element_present(i):
                    self.ew.tap_element(i)
                    break
                elif i == "Existing Item: transfer-every year":
                    self.create_transfer(amount="random", outgoing_wallet=None, incoming_wallet=None, start_date=None,
                                         note=None, recurrence="random", end_date=None, reminder=None)
                    self.transaction_actions.save_transaction()
                    self.timeline_general.open_scheduled_section()
                    for i in self.EXISTING_TRANSFER_TEMPLATES:
                        if self.ew.is_element_present(i):
                            self.ew.tap_element(i)
        else:
            self.create_transfer(amount="random", outgoing_wallet=None, incoming_wallet=None, start_date=None,
                                 note=None, recurrence="random", end_date=None, reminder=None)
            self.transaction_actions.save_transaction()
            self.timeline_general.open_scheduled_section()
            for i in self.EXISTING_TRANSFER_TEMPLATES:
                if self.ew.is_element_present(i):
                    self.ew.tap_element(i)

    def edit_transfer(self, transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence,
                      end_date, reminder):
        if transaction_type is not None:
            self.ew.tap_element(self.transaction_detail.CATEGORY_ICON)
            if transaction_type == "transfer":
                self.transaction_detail.set_type_to_transfer()
            else:
                self.transaction_detail.set_type_of_transaction(transaction_type)
                self.transaction_detail.set_category("random")
        if amount is not None:
            self.ew.tap_element(self.transaction_detail.AMOUNT_INPUT)
            self.ew.wait_till_element_is_visible(self.transaction_detail.NUMPAD_CLEAR, 10)
            for i in range(6):
                self.ew.wait_and_tap_element(self.transaction_detail.NUMPAD_CLEAR, 5)
            self.transaction_detail.set_amount(amount)
        if outgoing_wallet is not None:
            if self.transaction_detail.get_wallet("transfer_outgoing") == "Out of Spendee":
                self.transaction_detail.set_wallet(outgoing_wallet, "transfer_outgoing")
        if incoming_wallet is not None:
            if self.transaction_detail.get_wallet("transfer_incoming") == "Out of Spendee":
                self.transaction_detail.set_wallet(incoming_wallet, "transfer_incoming")
        if start_date is not None:
            self.transaction_detail.set_start_date(start_date)
        if note is not None:
            try:
                self.ew.get_element(self.transaction_detail.EXISTING_NOTE).clear()
            except NoSuchElementException:
                pass
            self.transaction_detail.set_note(note)
        if recurrence is not None:
            self.transaction_detail.set_recurrence(recurrence)
        if end_date is not None:
            self.transaction_detail.set_end_date(end_date)
        if reminder is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.REMINDER)
            self.transaction_detail.set_reminder(reminder)
        self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
