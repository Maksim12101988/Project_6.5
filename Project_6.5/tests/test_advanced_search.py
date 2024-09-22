import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
import logging
from config.settings import LOG_FILE, LOG_LEVEL

logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL),
                    format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.mark.usefixtures("web_driver_setup")
class TestAdvancedSearch:
    @pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
    def test_advanced_search(self, web_driver_setup):
        driver = web_driver_setup

        logging.info("Тест начат: Расширенный поиск на GitHub")

        with pytest.allure.step("Открытие страницы расширенного поиска"):
            driver.get("https://github.com/search/advanced")
            logging.info("Страница расширенного поиска открыта")

        try:
            with pytest.allure.step("Выбор языка Python"):
                language_select = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "search_language"))
                )
                language_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//select[@id='search_language']/optgroup[1]/option[19]"))
                )
                language_option.click()
                logging.info("Выбран язык Python")

            with pytest.allure.step("Ввод количества звезд (>20000)"):
                stars_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "search_stars"))
                )
                stars_input.clear()
                stars_input.send_keys(">20000")
                logging.info("Установлено количество звезд >20000")

            with pytest.allure.step("Ввод названия файла (environment.yml)"):
                filename_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "search_filename"))
                )
                filename_input.send_keys("environment.yml")
                logging.info("Указано название файла environment.yml")

            with pytest.allure.step("Нажатие кнопки поиска"):
                search_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                "#search_form > div.container-lg.p-responsive.advanced-search-form > div > div > button"))
                )
                search_button.click()
                logging.info("Нажата кнопка поиска")

            with pytest.allure.step("Проверка результата поиска"):
                WebDriverWait(driver, 15).until(
                    EC.url_contains(
                        "https://github.com/search?q=stars%3A%3E20000+path%3A**%2Fenvironment.yml+language%3APython&type=Repositories&ref=advsearch&l=Python&l=")
                )
                assert driver.current_url == "https://github.com/search?q=stars%3A%3E20000+path%3A**%2Fenvironment.yml+language%3APython&type=Repositories&ref=advsearch&l=Python&l=", "URL результата поиска не соответствует ожидаемому"
                logging.info("Результат поиска успешно проверен")

        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {str(e)}")
            raise AssertionError(f"Ошибка при выполнении теста: {str(e)}")

        pytest.allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
