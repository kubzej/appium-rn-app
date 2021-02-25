from selenium.common.exceptions import NoSuchElementException

from element_wrapper import ElementWrapper
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from page_objects.timeline.transfer.origination_destination_modal import TransferDestinationModal


class TransactionActions:
    EXISTING_TRANSACTION = "Existing Item: regular-undefined"
    EXISTING_TRANSACTION_TEMPLATES = ["Existing Item: regular-every day", "Existing Item: regular-every 2 days",
                                      "Existing Item: regular-every working day", "Existing Item: regular-every week",
                                      "Existing Item: regular-every 2 weeks", "Existing Item: regular-every 4 weeks",
                                      "Existing Item: regular-every month", "Existing Item: regular-every 2 months",
                                      "Existing Item: regular-every 3 months", "Existing Item: regular-every 6 months",
                                      "Existing Item: regular-every year"]

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.transfer_destination_modal = TransferDestinationModal(self.driver)


    def create_transaction(self, transaction_type, category, amount, currency, wallet, start_date, note, label, photo,
                           recurrence, end_date, reminder):
        """
        Opens create transaction screen and sets requested attributes
        :param transaction_type: str or None
        :param category: str or None
        :param amount: str or None
        :param currency: str or None
        :param wallet: str or None
        :param start_date: str or None
        :param note: str or None
        :param label: str or None
        :param photo: bool
        :param recurrence: str or None
        :param end_date: str or None
        :param reminder: str or None
        """
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
        if recurrence is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.RECURRENCE)
            self.transaction_detail.set_recurrence(recurrence)
        if end_date is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.END_DATE)
            self.transaction_detail.set_end_date(end_date)
        if reminder is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.REMINDER)
            self.transaction_detail.set_reminder(reminder)
        self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)

    def save_transaction(self):
        """Clicks on save transaction button"""
        self.ew.wait_and_tap_element(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
        if self.transfer_destination_modal.is_destination_modal_present() or self.transfer_destination_modal.is_origination_modal_present():
            self.transfer_destination_modal.create_as_new_transaction()

    def open_transaction(self):
        """Opens existing transaction, if there is no one, it creates transaction"""
        self.ew.wait_till_element_is_visible(self.timeline_general.OVERVIEW_BUTTON, 30)
        self.timeline_general.go_to_timeline()
        if self.ew.is_element_present(self.EXISTING_TRANSACTION) is False:
            self.create_transaction(transaction_type="random", category="random", amount="random", currency=None,
                                    wallet=None, start_date=None, note=None, label=None, photo=None, recurrence=None,
                                    end_date=None, reminder=None)
            self.save_transaction()
            self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)
        self.ew.wait_and_tap_element(self.EXISTING_TRANSACTION, 15)
        self.ew.wait_till_element_is_visible(self.transaction_detail.TRANSACTION_HEADER_TITLE, 15)

    def open_transaction_template(self):
        """Opens existing transaction template, if there is no one, it creates transaction"""
        self.ew.wait_till_element_is_visible(self.timeline_general.TRANSACTION_SECTION, 60)
        if self.ew.is_element_present(self.timeline_general.SCHEDULED) is True:
            self.timeline_general.open_scheduled_section()
            for i in self.EXISTING_TRANSACTION_TEMPLATES:
                if self.ew.is_element_present(i):
                    self.ew.tap_element(i)
                    break
                elif i == "Existing Item: regular-every year":
                    self.create_transaction(transaction_type="random", category="random", amount="random",
                                            currency=None,
                                            wallet=None, start_date=None, note=None, label=None, photo=None,
                                            recurrence="random", end_date=None, reminder=None)
                    self.save_transaction()
                    self.timeline_general.open_scheduled_section()
                    for i in self.EXISTING_TRANSACTION_TEMPLATES:
                        if self.ew.is_element_present(i):
                            self.ew.tap_element(i)
        else:
            self.create_transaction(transaction_type="random", category="random", amount="random", currency=None,
                                    wallet=None, start_date=None, note=None, label=None, photo=None,
                                    recurrence="random", end_date=None, reminder=None)
            self.save_transaction()
            self.timeline_general.open_scheduled_section()
            for i in self.EXISTING_TRANSACTION_TEMPLATES:
                if self.ew.is_element_present(i):
                    self.ew.tap_element(i)

    def edit_transaction(self, transaction_type, category, amount, wallet, start_date, note, label, photo, recurrence,
                         end_date, reminder):
        """Edits requested attributes on transaction detail screen
        :param transaction_type: str or None
        :param category: str or None
        :param amount: str or None
        :param wallet: str or None
        :param start_date: str or None
        :param note: str or None
        :param label: str or None
        :param photo: bool
        :param recurrence: str or None
        :param end_date: str or None
        :param reminder: str or None
        """
        if transaction_type is not None:
            self.ew.wait_and_tap_element(self.transaction_detail.CATEGORY_ICON, 10)
            if transaction_type == "transfer":
                self.transaction_detail.set_type_to_transfer()
            else:
                self.transaction_detail.set_type_of_transaction(transaction_type)
                self.transaction_detail.set_category("random")
        if category is not None:
            self.ew.wait_and_tap_element(self.transaction_detail.CATEGORY_ICON, 10)
            self.transaction_detail.set_category(category)
        if amount is not None:
            self.ew.wait_and_tap_element(self.transaction_detail.AMOUNT_INPUT, 10)
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
                self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
                self.ew.get_element(self.transaction_detail.EXISTING_NOTE).clear()
            except NoSuchElementException:
                pass
            self.transaction_detail.set_note(note)
        if label is not None:
            self.transaction_detail.set_label(label)
        if photo is not None:
            self.transaction_detail.set_photo()
        if recurrence is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.RECURRENCE)
            self.transaction_detail.set_recurrence(recurrence)
        if end_date is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.END_DATE)
            self.transaction_detail.set_end_date(end_date)
        if reminder is not None:
            self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)
            self.ew.swipe_if_element_not_present(self.transaction_detail.REMINDER)
            self.transaction_detail.set_reminder(reminder)
        self.ew.wait_till_element_is_visible(self.transaction_detail.SAVE_TRANSACTION_BUTTON, 5)

    def delete_transaction(self):
        """Deletes transaction from transaction detail screen"""
        self.ew.wait_and_tap_element(self.transaction_detail.TRASH_ICON, 10)
        self.ew.wait_and_tap_element(self.transaction_detail.DELETE_BUTTON, 10)
