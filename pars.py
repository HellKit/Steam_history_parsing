from selenium import webdriver
from time import sleep


def write_in_file(file_name, data):
    """Производит запись в файл"""
    with open(file_name, 'a',  encoding='utf') as f:
        f.write(f'{data}\n')


def get_first_settings():
    """Добавляет опции (настройки) для Хрома"""
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    driver.set_window_size(1920, 1080)
    return driver


def read_data_on_steam(driver):
    """Чтение данных из STEAM"""
    # создаем список с товарами из истории сделок
    elements = driver.find_elements_by_class_name('market_recent_listing_row')
    # убираем лишнии товары, так как с таким же классом есть еще несколько товаров
    # которые нам не нужны
    elements = elements[:len(elements)-10] if len(elements) > 10 else elements
    for element in elements:
        result_cell = element.find_element_by_class_name('market_listing_left_cell').text.strip()
        result_cell = result_cell if len(result_cell) != 0 else None
        if not result_cell:
            continue
        # используем tuple, чтобы не сильно нагружать память
        data = (
            'Куплено' if result_cell == '+' else 'Продано',
            element.find_element_by_class_name(
                'market_listing_item_name').text.strip(),
            element.find_element_by_class_name(
                'market_listing_price').text.strip(),
        )
        write_in_file('steam_data.txt', '  --->  '.join(data))


def last_page(driver):
    """Последнаяя страница списка истории сделок
    Возвращает целое число"""
    return int(driver.find_elements_by_class_name('market_paging_pagelink')[-1].text.strip())


def click_next_slide(driver):
    """Производит нажатие на следующую страницу истории"""
    driver.execute_script(
        'arguments[0].click();', driver.find_element_by_id(
            'tabContentsMyMarketHistory_btn_next'))


################################################################################################
driver = get_first_settings()
# получаем доступ к авторизации
driver.get('https://steamcommunity.com/login/home/?goto=')

sleep(50)  # время для захода в STEAM, можно менять, главное успеть зайти

for _ in range(last_page(driver)):
    read_data_on_steam(driver)
    click_next_slide(driver)
    sleep(5)
