import allure
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType
import logging
from config.settings import LOG_FILE, LOG_LEVEL

logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

@pytest.mark.usefixtures("driver")
class TestGitHubCommitActivity:
    @pytest.allure.severity(pytest.allure.severity_level.NORMAL)
    def test_github_commit_activity(self, driver):
        logging.info("Тест начат: Проверка активности коммитов на GitHub")

        with pytest.allure.step("Открытие страницы активности коммитов"):
            url = "https://github.com/microsoft/vscode/graphs/commit-activity"
            driver.get(url)
            logging.info("Страница активности коммитов открыта")

        try:
            with pytest.allure.step("Поиск элемента для клика"):
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#commit-activity-master > svg > g > g.bar.mini.active > rect"))
                )
                logging.info("Элемент найден и готов к клику")

            with pytest.allure.step("Клик по элементу"):
                element.click()
                logging.info("Нажатие на элемент выполнено успешно")

            with pytest.allure.step("Ожидание появления всплывающей подсказки"):
                tooltip = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'svg-tip') and contains(@class, 'n')]"))
                )
                logging.info("Всплывающая подсказка успешно отображена")

        except TimeoutException:
            logging.error("Всплывающая подсказка не появилась в течение указанного времени.")
            assert False, "Всплывающая подсказка не появилась в течение указанного времени."
        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {str(e)}")
            raise AssertionError(f"Ошибка при выполнении теста: {str(e)}")

        logging.info("Тест пройден успешно!")
        pytest.allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
