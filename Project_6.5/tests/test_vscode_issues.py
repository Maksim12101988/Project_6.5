import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from allure_commons.types import AttachmentType
import logging
from config.settings import LOG_FILE, LOG_LEVEL

logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL),
                    format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.mark.usefixtures("web_driver_setup")
class TestVSCodeIssuesSearch:
    @pytest.allure.severity(pytest.allure.severity_level.NORMAL)
    def test_vscode_issues_search(self, web_driver_setup):
        driver = web_driver_setup

        logging.info("Тест начат: Поиск проблем в VSCode")

        with pytest.allure.step("Открытие страницы проблем VSCode"):
            driver.get("https://github.com/microsoft/vscode/issues")
            logging.info("Страница проблем VSCode открыта")

        try:
            with pytest.allure.step("Поиск проблем с ключевым словом 'bug'"):
                search_input = driver.find_element(By.ID, "js-issues-search")
                search_input.send_keys("in:title bug")
                search_input.send_keys(Keys.RETURN)
                logging.info("Выполнен поиск проблем с ключевым словом 'bug'")

            with pytest.allure.step("Проверка результата поиска"):
                assert "bug" in driver.page_source, "Проблемы с ключевым словом 'bug' не найдены"
                logging.info("Результат поиска успешно проверен")

        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {str(e)}")
            raise AssertionError(f"Ошибка при выполнении теста: {str(e)}")

        pytest.allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
