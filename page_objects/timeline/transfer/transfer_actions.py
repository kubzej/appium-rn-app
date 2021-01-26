from element_wrapper import ElementWrapper
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail


class TransferActions():

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)

    def create_transfer(self, amount, outgoing_wallet, incoming_wallet, start_date, note, reminder):
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
        if reminder is not None:
            self.transaction_detail.set_reminder(reminder)
