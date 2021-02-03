import desired_capabilities
import pytest
from appium import webdriver

PLATFORM = "Android"
# PLATFORM = "iOS"


@pytest.fixture()
def driver_with_reset(request):
    url = "http://localhost:4723/wd/hub"
    if PLATFORM == "Android":
        capabilities = desired_capabilities.get_desired_capabilities_android(no_reset=False)
    else:
        capabilities = desired_capabilities.get_desired_capabilities_ios(no_reset=False)

    request.instance.driver = webdriver.Remote(url, capabilities)

    def tearDown():
        request.instance.driver.quit()

    request.addfinalizer(tearDown)


@pytest.fixture()
def driver_without_reset(request):
    url = "http://localhost:4723/wd/hub"
    if PLATFORM == "Android":
        capabilities = desired_capabilities.get_desired_capabilities_android(no_reset=True)
    else:
        capabilities = desired_capabilities.get_desired_capabilities_ios(no_reset=True)

    request.instance.driver = webdriver.Remote(url, capabilities)

    def tearDown():
        request.instance.driver.quit()

    request.addfinalizer(tearDown)
