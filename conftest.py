import pytest
from settings import valid_email, valid_password
from selenium import webdriver
driver = webdriver.Chrome()
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(r'C:\chromedriver/chromedriever.exe')

   # Переходим на страницу авторизации
   pytest.driver.get('https://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


@pytest.fixture()
def go_to_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Нажимаем на ссылку "Мои питомцы"
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()