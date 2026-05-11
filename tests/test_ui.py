from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    page = Path(__file__).resolve().parent.parent / "index.html"
    driver.get(page.as_uri())
    yield driver
    driver.quit()


def test_title_exists(driver):
    assert driver.find_element(By.ID, "title").text == "Форма обратной связи"


def test_empty_form_shows_error(driver):
    driver.find_element(By.ID, "submit").click()
    assert driver.find_element(By.ID, "result").text == "Проверьте данные"


def test_invalid_email_shows_error(driver):
    driver.find_element(By.ID, "name").send_keys("Иван")
    driver.find_element(By.ID, "email").send_keys("ivanmail.com")
    driver.find_element(By.ID, "submit").click()
    assert driver.find_element(By.ID, "result").text == "Проверьте данные"


def test_valid_data_shows_success(driver):
    driver.find_element(By.ID, "name").send_keys("Иван")
    driver.find_element(By.ID, "email").send_keys("ivan@mail.com")
    driver.find_element(By.ID, "submit").click()
    assert driver.find_element(By.ID, "result").text == "Форма отправлена"
