import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from allure_commons.types import AttachmentType
import logging
from config.settings import LOG_FILE, LOG_LEVEL

logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL),
                    format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.mark.usefixtures("web_driver_setup")
class TestAuthorBpaseroIssues:
    @pytest.allure.severity(pytest.allure.severity_level.NORMAL)
    def test_author_bpasero_issues(self, web_driver_setup):
        driver = web_driver_setup

        logging.info("Тест начат: Поиск проблем bpasero на GitHub")

        with pytest.allure.step("Открытие страницы проблем VSCode"):
            driver.get("https://github.com/microsoft/vscode/issues")
            logging.info("Страница проблем VSCode открыта")

        try:
            with pytest.allure.step("Нажатие на элемент выбора автора"):
                author_select_menu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='author-select-menu']/summary/span"))
                )
                author_select_menu.click()
                logging.info("Нажато на элемент выбора автора")

            with pytest.allure.step("Ввод имени пользователя bpasero"):
                author_filter_field = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='author-filter-field']"))
                )
                actions = ActionChains(driver)
                actions.move_to_element(author_filter_field).click().send_keys("bpasero").perform()
                logging.info("Введено имя пользователя bpasero и нажата Enter")

            # Добавьте здесь дополнительные проверки или действия, если необходимо

        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {str(e)}")
            raise AssertionError(f"Ошибка при выполнении теста: {str(e)}")

        pytest.allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
