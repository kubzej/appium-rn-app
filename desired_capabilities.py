import os

import secrets as s


def PATH(p):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )


def get_desired_capabilities_android(no_reset):
    desired_caps = {
        'platformName': 'Android',
        'app': s.app_android,
        'automationName': 'uiautomator2',
        'deviceName': 'Android emulator',
        'noReset': no_reset,
        'udid': "emulator-5554",
    }
    return desired_caps


def get_desired_capabilities_ios(no_reset):
    desired_caps = {
        'platformName': 'iOS',
        'app': s.app_ios,
        'automationName': 'XCUITest',
        'deviceName': 'iPhone 11',
        'platformVersion': '14.4',
        'noReset': no_reset,
        "xcodeOrgId": s.xcode_org_id,
        "xcodeSigningId": s.xcode_signing_id
    }
    return desired_caps
