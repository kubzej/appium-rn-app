from element_wrapper import ElementWrapper
from conftest import PLATFORM


class Google():

    if PLATFORM == "Android":
        EMAIL_TO_SELECT = '//hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/' \
                          'android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/' \
                          'android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]'
    else:
        EMAIL_TO_SELECT

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)