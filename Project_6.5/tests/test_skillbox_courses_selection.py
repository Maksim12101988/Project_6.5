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
class TestSkillboxCoursesSelection:
    @pytest.allure.severity(pytest.allure.severity_level.NORMAL)
    def test_skillbox_courses_selection(self, web_driver_setup):
        driver = web_driver_setup

        logging.info("Тест начат: Выбор курсов на Skillbox")

        with pytest.allure.step("Открытие страницы курсов программирования"):
            driver.get("https://skillbox.ru/code/")
            logging.info("Страница курсов программирования открыта")

        try:
            with pytest.allure.step("Выбор типа обучения"):
                education_type_radio = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//*[@id='#app']/main/div[1]/div[2]/div/div[1]/div[1]/div[2]/ul/li[2]/label/span"))
                )
                education_type_radio.click()
                logging.info("Выбран тип обучения")

            with pytest.allure.step("Установка длительности курса"):
                duration_slider_6_months = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[@id='#app']/main/div[1]/div[2]/div/div[1]/div[1]/div[5]/div[2]/div[2]/div/div[2]/button"))
                )
                duration_slider_6_months.click()

                duration_slider_12_months = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[@id='#app']/main/div[1]/div[2]/div/div[1]/div[1]/div[5]/div[2]/div[2]/div/div[3]/button"))
                )
                duration_slider_12_months.click()
                logging.info("Установлена длительность курса")

            with pytest.allure.step("Выбор тематики"):
                theme_checkbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[@id='#app']/main/div[1]/div[2]/div/div[1]/div[1]/div[5]/div[2]/div[2]/div/div[3]/button"))
                )
                theme_checkbox.click()
                logging.info("Выбрана тематика")

            with pytest.allure.step("Переход на страницу конкретного курса"):
                course_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[@id='#app']/main/div[1]/div[2]/div/div[1]/div[1]/div[5]/div[2]/div[2]/div/div[3]/button"))
                )
                course_link.click()
                logging.info("Перешли на страницу конкретного курса")

        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {str(e)}")
            raise AssertionError(f"Ошибка при выполнении теста: {str(e)}")

        pytest.allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
