import logging
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import LOG_FILE, LOG_LEVEL

logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="session")
def web_driver_setup(request):
    chrome_options = Options()
    chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    driver = webdriver.Chrome(options=chrome_options)

    logging.info("Браузер запущен")

    def fin():
        logging.info("Тесты завершены. Браузер закрывается.")
        driver.quit()

    request.addfinalizer(fin)
    return driver

def pytest_configure(config):
    pass

def allure_report(driver):
    yield
    allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

@pytest.hookimpl
def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # execute all other hooks to obtain the report object
        report = pytest_runtest_makereport.makereport(item, call)
        if call.excinfo:
            # we only look at actual failures, not setup/teardown
            if (call.start == call.stop):
                test_failed = item._previousfailed
                print("runtest_makereport", test_failed)
                if test_failed:
                    print("Rerun:", item.name)
                    pytest.xfail("xfail-marked test failed on rerun")
        return report

