import time

from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.timeline.filters.period_filter import PeriodFilter
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from page_objects.timeline.transaction.transaction_validator import TransactionValidator
from page_objects.timeline.transaction_template.transaction_template_validator import TransactionTemplateValidator
from page_objects.timeline.transfer.transfer_validator import TransferValidator
from resolutions import Resolutions


class TransferTemplateValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.period_filter = PeriodFilter(self.driver)
        self.rs = Resolutions(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.transaction_template_validator = TransactionTemplateValidator(self.driver)
        self.transaction_validator = TransactionValidator(self.driver)
        self.transfer_validator = TransferValidator(self.driver)

    def get_all_attributes(self):
        """ Getting all attributes of transfer template
        :return: dict
        """
        all_attributes = {"amount": self.transaction_detail.get_amount(),
                          "currency": self.transaction_detail.get_currency(),
                          "wallet_amount": self.transaction_detail.get_wallet_amount(),
                          "outgoing_wallet": self.transaction_detail.get_wallet("transfer_outgoing"),
                          "incoming_wallet": self.transaction_detail.get_wallet("transfer_incoming"),
                          "start_date": self.transaction_detail.get_date("start"),
                          "note": self.transaction_detail.get_note(),
                          "recurrence": self.transaction_detail.get_recurrence(),
                          "end_date": self.transaction_detail.get_date("end"),
                          "reminder": self.transaction_detail.get_reminder(),
                          }

        return all_attributes

    def is_transfer_template_on_timeline(self, attributes):
        """ Checking if transfer template is visible inside Scheduled section
        :param attributes: dict
        :return: bool
        """
        if "Out of Spendee" not in [attributes['outgoing_wallet'], attributes['incoming_wallet']]:
            is_two_way_transfer = True
        else:
            is_two_way_transfer = False

        transfer_locator = f"transfer/" \
                           f"undefined/" \
                           f"{self.transfer_validator.adjust_amounts(attributes['amount'], attributes['wallet_amount'], attributes['currency'], attributes['outgoing_wallet'], attributes['incoming_wallet'])[0]}/" \
                           f"{self.transfer_validator.adjust_amounts(attributes['amount'], attributes['wallet_amount'], attributes['currency'], attributes['outgoing_wallet'], attributes['incoming_wallet'])[1]}/" \
                           f"{self.transfer_validator.adjust_wallets(attributes['outgoing_wallet'], attributes['incoming_wallet'])[0]}/" \
                           f"{self.transfer_validator.adjust_wallets(attributes['outgoing_wallet'], attributes['incoming_wallet'])[1]}/" \
                           f"{self.transaction_validator.adjust_note(attributes['note'])}/" \
                           f"undefined/" \
                           f"false/" \
                           f"{self.transaction_template_validator.adjust_recurrence(attributes['recurrence'])}/" \
                           f"{self.transaction_template_validator.adjust_end_date(attributes['end_date'])}/" \
                           f"{self.transaction_validator.adjust_reminder(attributes['reminder'])}"

        print(f'LOCATOR: {transfer_locator}')

        if is_two_way_transfer:
            _, _, amount, wallet_amount, outgoing_wallet, incoming_wallet, _, _, _, recurrence, _, _ = (str(x) for x in
                                                                                                        transfer_locator.split(
                                                                                                            '/'))
            s_out = transfer_locator.split("/")
            s_in = transfer_locator.split("/")

            s_out[2] = f"-{amount}"
            if wallet_amount != "undefined":
                s_out[3] = f"-{wallet_amount}"

            if recurrence == "undefined":
                s_in[4] = incoming_wallet
                s_in[5] = outgoing_wallet

            transfer_outgoing_locator = '/'.join(s_out)
            transfer_incoming_locator = '/'.join(s_in)

            print(f'OUTGOING LOCATOR: {transfer_outgoing_locator}')
            print(f'INCOMING LOCATOR: {transfer_incoming_locator}')

        self.transaction_validator.prepare_timeline(attributes['start_date'],
                                                    self.transaction_template_validator.adjust_recurrence(
                                                        attributes['recurrence']))

        android_timeout = time.time() + 60
        ios_timeout = time.time() + 5
        res = self.rs.get_resolution()

        if is_two_way_transfer:
            locator = transfer_outgoing_locator
        else:
            locator = transfer_locator
        is_transfer_present = self.ew.is_element_present(locator)
        while is_transfer_present is False:
            if PLATFORM == "Android":
                self.transaction_validator.swipe_android(res)
                is_transfer_present = self.ew.is_element_present(locator)
                if time.time() > android_timeout:
                    return False
            else:
                is_transfer_present = self.ew.is_element_present(locator)
                if time.time() > ios_timeout:
                    return False
        if is_two_way_transfer and self.ew.is_element_present(transfer_incoming_locator) is False:
            return False
        return True
