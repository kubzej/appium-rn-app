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
            "phones": ["iPhone 11"]
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
            "phones": ["Samsung S20"]
        }
    }

    def __init__(self, driver):
        self.driver = driver

    def get_resolution(self):
        d = self.driver.get_window_size()
        res = f"{d['width']}_{d['height']}"
        if res in self.all_resolutions:
            return res
        else:
            raise NotImplemented(f"Not implemented resolution of phone.")
