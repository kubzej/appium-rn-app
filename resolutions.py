class Resolutions:
    all_resolutions = {
        "414_896": {
            "x": 100,
            "calendar_picker_up_y_start": 700,
            "calendar_picker_up_y_end": 570,
            "calendar_picker_down_y_start": 700,
            "calendar_picker_down_y_end": 830,
            "default_picker_up_y_start": 850,
            "default_picker_up_y_end": 820,
            "element_not_present_swipe_y_start": 750,
            "element_not_present_swipe_y_end": 450,
            "transaction_timeline_up_y_start": 800,
            "transaction_timeline_up_y_end": 400,
            "budget_overview_y_start": 800,
            "budget_overview_y_end": 400,
            "wallets_overview_y_start": 800,
            "wallets_overview_y_end": 400,
            "categories_y_start": 800,
            "categories_y_end": 400,
            "phones": ["iPhone 11 Pro", "iPhone 11 X", "iPhone Xs"]
        },
        "375_812": {
            "x": 100,
            "calendar_picker_up_y_start": 650,
            "calendar_picker_up_y_end": 515,
            "calendar_picker_down_y_start": 650,
            "calendar_picker_down_y_end": 770,
            "default_picker_up_y_start": 780,
            "default_picker_up_y_end": 750,
            "element_not_present_swipe_y_start": 700,
            "element_not_present_swipe_y_end": 410,
            "transaction_timeline_up_y_start": 750,
            "transaction_timeline_up_y_end": 400,
            "budget_overview_y_start": 750,
            "budget_overview_y_end": 400,
            "wallets_overview_y_start": 750,
            "wallets_overview_y_end": 400,
            "categories_y_start": 750,
            "categories_y_end": 400,
            "phones": ["iPhone 11", "iPhone 11 Pro Max", "iPhone Xs Max"]
        },
        "414_736": {
            "x": 100,
            "calendar_picker_up_y_start": 625,
            "calendar_picker_up_y_end": 490,
            "calendar_picker_down_y_start": 625,
            "calendar_picker_down_y_end": 740,
            "default_picker_up_y_start": 750,
            "default_picker_up_y_end": 710,
            "element_not_present_swipe_y_start": 675,
            "element_not_present_swipe_y_end": 400,
            "transaction_timeline_up_y_start": 690,
            "transaction_timeline_up_y_end": 390,
            "budget_overview_y_start": 690,
            "budget_overview_y_end": 390,
            "wallets_overview_y_start": 690,
            "wallets_overview_y_end": 390,
            "categories_y_start": 690,
            "categories_y_end": 390,
            "phones": ["iPhone 8+", "iPhone 6+", "iPhone 7+"]
        },
        "1080_1794": {
            "x": 100,
            "calendar_picker_up_y_start": 1780,
            "calendar_picker_up_y_end": 825,
            "calendar_picker_down_y_start": 1275,
            "calendar_picker_down_y_end": 1750,
            "default_picker_up_y_start": 1780,
            "default_picker_up_y_end": 1150,
            "element_not_present_swipe_y_start": 1600,
            "element_not_present_swipe_y_end": 1200,
            "transaction_timeline_up_y_start": 1650,
            "transaction_timeline_up_y_end": 300,
            "budget_overview_y_start": 1650,
            "budget_overview_y_end": 300,
            "wallets_overview_y_start": 1650,
            "wallets_overview_y_end": 300,
            "categories_y_start": 1650,
            "categories_y_end": 300,
            "phones": ["Pixel 2"]
        },
        "1080_1997": {
            "x": 100,
            "calendar_picker_up_y_start": 1980,
            "calendar_picker_up_y_end": 770,
            "calendar_picker_down_y_start": 1370,
            "calendar_picker_down_y_end": 1980,
            "default_picker_up_y_start": 1980,
            "default_picker_up_y_end": 1160,
            "element_not_present_swipe_y_start": 1500,
            "element_not_present_swipe_y_end": 1100,
            "transaction_timeline_up_y_start": 1650,
            "transaction_timeline_up_y_end": 300,
            "budget_overview_y_start": 1760,
            "budget_overview_y_end": 415,
            "wallets_overview_y_start": 1760,
            "wallets_overview_y_end": 415,
            "categories_y_start": 1760,
            "categories_y_end": 415,
            "phones": ["Samsung S20"]
        },
        "1440_2960": {
            "x": 200,
            "calendar_picker_up_y_start": 2940,
            "calendar_picker_up_y_end": 1450,
            "calendar_picker_down_y_start": 1890,
            "calendar_picker_down_y_end": 2940,
            "default_picker_up_y_start": 2940,
            "default_picker_up_y_end": 1650,
            "element_not_present_swipe_y_start": 1900,
            "element_not_present_swipe_y_end": 1620,
            "transaction_timeline_up_y_start": 2150,
            "transaction_timeline_up_y_end": 400,
            "budget_overview_y_start": 2640,
            "budget_overview_y_end": 550,
            "wallets_overview_y_start": 2640,
            "wallets_overview_y_end": 550,
            "categories_y_start": 2640,
            "categories_y_end": 550,
            "phones": ["Samsung S8", "Samsung S9", "Samsung S9+", "Samsung Note9"]
        }
    }

    def __init__(self, driver):
        self.driver = driver

    def get_resolution(self):
        """ Gets width and height of phone screen
        :return: str
        """
        d = self.driver.get_window_size()
        res = f"{d['width']}_{d['height']}"
        if res in self.all_resolutions:
            return res
        else:
            raise NotImplemented(f"Not implemented resolution of phone.")
