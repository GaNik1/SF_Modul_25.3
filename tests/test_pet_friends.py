# Практическое задание: 25.3
# python -m pytest -v --driver Chrome --driver-path tests/chromedriver.exe tests/test_pet_friends.py

import pytest
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password

def test_petfriends_login():
    '''Проверяем что мы удачно автоматизировались"'''
    result = pytest.driver.find_element(By.CSS_SELECTOR, 'h1').text
    assert result == "PetFriends", "login error"


def test_show_my_pets():
   '''Проверяем что мы оказались на странице "Мои питомцы"'''

   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Нажимаем на ссылку "Мои питомцы"
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

   # Проверяем что мы оказались на странице "Мои питомцы"
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'


def test_all_pets_are_present(go_to_my_pets):
   '''Проверяем что на странице со списком моих питомцев присутствуют все питомцы'''

   # Сохраняем в переменную ststistic элементы статистики
   statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

   # Сохраняем в переменную pets элементы карточек питомцев
   pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Получаем количество питомцев из данных статистики
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])

   # Получаем количество карточек питомцев
   number_of_pets = len(pets)

   # Проверяем что количество питомцев из статистики совпадает с количеством карточек питомцев
   assert number == number_of_pets


def test_photo_availability(go_to_my_pets):
   '''Поверяем что на странице со списком моих питомцев хотя бы у половины питомцев есть фото'''

   # Сохраняем в переменную ststistic элементы статистики
   statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

   # Сохраняем в переменную images элементы с атрибутом img
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

   # Получаем количество питомцев из данных статистики
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])

   # Находим половину от количества питомцев
   half = number // 2

   # Находим количество питомцев с фотографией
   number_а_photos = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         number_а_photos += 1

   # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
   assert number_а_photos >= half
   print(f'количество фото: {number_а_photos}')
   print(f'Половина от числа питомцев: {half}')


def test_petfriends_pets_cards(go_to_my_pets):
    '''Поверяем что на странице со списком моих питомцев, у всех питомцев есть имя, возраст и порода'''
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != '', 'Image not found'
        assert names[i].text != '', 'Name not found'
        assert descriptions[i].text != '', 'Description not found'
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0, 'Species not found'
        assert len(parts[1]) > 0, 'Age not found'


def test_all_pets_have_different_names(go_to_my_pets):
   '''Поверяем что на странице со списком моих питомцев, у всех питомцев разные имена'''

   # Сохраняем в переменную pet_data элементы с данными о питомцах
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем по пробелу.Выбераем имена и добавляем их в список pets_name.
   pets_name = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      pets_name.append(split_data_pet[0])

   # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
   # Проверяем, если r == 0 то повторяющихся имен нет.
   r = 0
   for i in range(len(pets_name)):
      if pets_name.count(pets_name[i]) > 1:
         r += 1
   assert r == 0
   print(r)
   print(pets_name)


def test_no_duplicate_pets(go_to_my_pets):
    '''Поверяем что на странице со списком моих питомцев нет повторяющихся питомцев'''

    # Сохраняем в переменную pet_data элементы с данными о питомцах
    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0
