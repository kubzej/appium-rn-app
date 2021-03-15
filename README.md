# Test automation of RN app using Appium

## Prerequisities
- Latest Appium - See [Install Appium on local machine](https://github.com/appium/appium/blob/master/docs/en/about-appium/getting-started.md)
- Python 3
- Builded RN app - See [RN app repository](https://gitlab.spendee.com/frontend/spendeern)
- Created `secrets.py` in root with requested [variables](#secrets.py).

## Running tests
1. Set preferred [capabilities](#capabilities)
2. [Start Appium server](https://github.com/appium/appium/blob/master/docs/en/about-appium/getting-started.md)
3. Inside `conftest.py` set preferable `PLATFORM` you want to run test on
4. Find folder with tests under  `/tests`
5. Run test via pytest module directly from IDE or [via command](https://docs.pytest.org/en/stable/usage.html)

### Desired capabilities
<a name="capabilities"></a>
| Android capabilities      | Description |
| ----------- | ----------- |
| platformName      | Android |
| app   | \<local path to the app file\> |
| automationName   | uiautomator2 |
| deviceName   | \<the kind of mobile device or emulator to use\> |
| platformVersion   | \<mobile OS version\> |
| noReset   | \<bool\> If true, reset app before new session |
| udid   | \<unique device id\> |

| iOS capabilities      | Description |
| ----------- | ----------- |
| platformName      | iOS |
| app   | \<local path to the app file\> |
| automationName   | XCUITest |
| deviceName   | \<the kind of mobile device or emulator to use\> |
| platformVersion   | \<mobile OS version\> |
| noReset   | \<bool\> If true, reset app before new session |
| xcodeOrgId   | \<team id\> |
| xcodeSigningId   | \<iPhone developer\> |


### secrets.py
<a name="secrets.py"></a>
This file should be created in root of project with these 4 variables

`app_android` = \<path to the Android app\> (usually created in app project /android/app/build/outputs/apk/devel/debug/app-devel-debug.apk)  
`app_ios` = \<path to the iOS app\> (usually created in app project /ios/build/Spendee-Devel/Build/Products/Devel.Debug-iphonesimulator/Spendee.app)  
`xcode_org_id` = \<[Team ID](https://appium.io/docs/en/drivers/ios-xcuitest-real-devices/)\>  
`xcode_signing_id`= \<[Developer ID](https://appium.io/docs/en/drivers/ios-xcuitest-real-devices/)\>

### Environmental variables
- `FACEBOOK_APP_ID` (Facebook app id of devel application)
- `FACEBOOK_SECRET` (Facebook secret of devel application)

### Running real device or emulator/simulator
- For Android just specify correct `udid` for device you want to use. You can get active `udid` via adb command `adb devices`. You will get connected list of android devices.
- For iOS, if you want to launch tests on real device, you have to use `xcodeOrgId` and `xcodeSigningId` capabilities. Don't use them for simulator. 
