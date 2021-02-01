import time

from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.timeline.filters.period_filter import PeriodFilter
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from page_objects.timeline.transaction.transaction_validator import TransactionValidator
from resolutions import Resolutions


class TransferValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.period_filter = PeriodFilter(self.driver)
        self.rs = Resolutions(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.transaction_validator = TransactionValidator(self.driver)

    def get_all_attributes(self):
        all_attributes = {"amount": self.transaction_detail.get_amount(),
                          "currency": self.transaction_detail.get_currency(),
                          "wallet_amount": self.transaction_detail.get_wallet_amount(),
                          "outgoing_wallet": self.transaction_detail.get_wallet("transfer_outgoing"),
                          "incoming_wallet": self.transaction_detail.get_wallet("transfer_incoming"),
                          "start_date": self.transaction_detail.get_date("start"),
                          "note": self.transaction_detail.get_note(),
                          "reminder": self.transaction_detail.get_reminder(),
                          }

        return all_attributes

    def is_transfer_on_timeline(self, attributes):
        if "Out of Spendee" not in [attributes['outgoing_wallet'], attributes['incoming_wallet']]:
            is_two_way_transfer = True
        else:
            is_two_way_transfer = False

        transfer_locator = f"transfer/" \
                           f"undefined/" \
                           f"{self.adjust_amounts(attributes['amount'], attributes['wallet_amount'], attributes['currency'], attributes['outgoing_wallet'], attributes['incoming_wallet'])[0]}/" \
                           f"{self.adjust_amounts(attributes['amount'], attributes['wallet_amount'], attributes['currency'], attributes['outgoing_wallet'], attributes['incoming_wallet'])[1]}/" \
                           f"{self.adjust_wallets(attributes['outgoing_wallet'], attributes['incoming_wallet'])[0]}/" \
                           f"{self.adjust_wallets(attributes['outgoing_wallet'], attributes['incoming_wallet'])[1]}/" \
                           f"{self.transaction_validator.adjust_note(attributes['note'])}/" \
                           f"undefined/" \
                           f"false/" \
                           f"undefined/" \
                           f"undefined/" \
                           f"{self.transaction_validator.adjust_reminder(attributes['reminder'])}"

        print(f'LOCATOR: {transfer_locator}')

        if is_two_way_transfer:
            _, _, amount, wallet_amount, outgoing_wallet, incoming_wallet, _, _, _, _, _, _ = (str(x) for x in
                                                                                               transfer_locator.split(
                                                                                                   '/'))
            s_out = transfer_locator.split("/")
            s_in = transfer_locator.split("/")

            s_out[2] = f"-{amount}"
            if wallet_amount != "undefined":
                s_out[3] = f"-{wallet_amount}"

            s_in[4] = incoming_wallet
            s_in[5] = outgoing_wallet

            transfer_outgoing_locator = '/'.join(s_out)
            transfer_incoming_locator = '/'.join(s_in)

        self.transaction_validator.prepare_timeline(attributes['start_date'])

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

    def adjust_amounts(self, amount, wallet_amount, currency, outgoing_wallet, incoming_wallet):
        if "Out of Spendee" in [outgoing_wallet, incoming_wallet]:
            oos_present = True
        else:
            oos_present = False

        if currency == "USD":
            amount_final = amount
            wallet_amount_final = "undefined"
        elif currency != "USD" and oos_present is False:
            amount_final = wallet_amount
            wallet_amount_final = "{:.2f}".format(float(amount))
        else:
            raise NotImplementedError(
                "Not implemented case for 1-way transfer with different currency than main USD currency")

        return ["{:.2f}".format(float(amount_final)), wallet_amount_final]

    def adjust_wallets(self, outgoing_wallet, incoming_wallet):
        p = [outgoing_wallet, incoming_wallet]
        wallets = [i if i != "Out of Spendee" else "undefined" for i in p]

        if wallets[0] == "undefined":
            wallets = [wallets[1], wallets[0]]

        return wallets
