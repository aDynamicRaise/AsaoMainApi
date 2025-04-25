import json
from datetime import datetime
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import os
from sqlalchemy.exc import IntegrityError
from database import get_async_session, Product, ProductData
from utils.repository import AbstractRepository
from config import msk_timezone
import traceback

from requests_html import HTMLSession
import json


class ProductService:
    def __init__(self, repo: AbstractRepository):
        self.repo: type[AbstractRepository] = repo

    async def get_product_name(self, product_id: int) -> str | None:
        return await self.repo.get_name_by_id(product_id)

    async def get_product_id(self, product_id: int) -> str | None:
        return await self.repo.get_id_by_id(product_id)
    

############# Пытался без селениума - напрямую обращаться
def search_ozon_products(item_name):
    session = HTMLSession()
    
    # Формируем URL для поиска
    url = f"https://www.ozon.ru/search/?text={item_name}"

    response = session.get(url)

    if response.status_code != 200:
        raise Exception(f"Ошибка запроса: {response.status_code}") # здесь кидает 403

    # Теперь мы можем получить HTML, который рендерится через JavaScript
    response.html.render()

    # Анализируем страницу на предмет товаров
    products = []
    items = response.html.find('.product-card')  # Или другой CSS-селектор, который указывает на карточку товара

    for item in items:
        product = {
            "title": item.find('.product-title', first=True).text if item.find('.product-title', first=True) else "Нет данных",
            "price": item.find('.price', first=True).text if item.find('.price', first=True) else "Нет данных",
            "url": item.find('a', first=True).attrs.get('href') if item.find('a', first=True) else "Нет данных",
            "image": item.find('img', first=True).attrs.get('src') if item.find('img', first=True) else "Нет данных",
        }
        products.append(product)

    return products
#############

# получить данные товаров по запросу (item_name)
# *amount_needed_items_max - по какому количеству товаров собрать данные, но парсинг может собрать и меньшее количество (TODO: сделать четкое количество)
async def get_products_data(item_name, amount_needed_items_max=10, date_receipt=datetime.now(msk_timezone).strftime("%Y-%m-%d %H:%M:%S")):
    # Настройка опций Chrome
    options = uc.ChromeOptions()
    
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")

    products_data = []
    product_urls = []
    driver = None

    try:
        driver = uc.Chrome(
            options=options
        )
        driver.implicitly_wait(10)

        driver.get(url='https://ozon.ru')
        time.sleep(2)

        # посмотреть что за страницу возвращает (сейчас - страницу с капчей, что very bad)
        print(driver.page_source[:1000])

        # Ожидание появления поля поиска
        find_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(3)

        product_urls_dict = {}

        try:
            # Ожидаем загрузку списка товаров
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'tile-clickable-element'))
            )

            # Получаем все ссылки товаров
            find_links = driver.find_elements(By.CLASS_NAME, 'tile-clickable-element')
            product_urls = list(set([
                f"{link.get_attribute('href')}"
                for link in find_links if link.get_attribute("href")
            ]))

            for k, v in enumerate(product_urls):
                product_urls_dict[k] = v

            print('[+] Ссылки на товары собраны!')
        except Exception as e:
            print(f'[-] Ошибка при сборке ссылок на товары: {e}')
            return products_data  # Возвращаем пустой список, если не удалось собрать ссылки

        with open('product_urls_dict.json', 'w', encoding='utf-8') as file:
            json.dump(product_urls_dict, file, indent=4, ensure_ascii=False)

        i = 0
        for url in product_urls:
            data = collect_product_info(driver=driver, date_receipt=date_receipt, url=url)
            if data:  # Проверяем, что данные собраны успешно
                print(f'[+] Собрал данные товара с id: {data.get("product_id")}')
                products_data.append(data)
                if i >= amount_needed_items_max - 1:  # Учитываем, что i начинается с 0
                    break
                i += 1
            time.sleep(2)

    except Exception as e:
        print(f'[-] Ошибка в процессе выполнения get_products_data: {e}')
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()  # Гарантированное правильное закрытие браузера

    return products_data

# получить данные товара по ссылке на карту товара (url) с указанием даты и времени сбора данных (date_receipt)
def collect_product_info(driver, date_receipt, url=''):
    try:
        driver.switch_to.new_window('tab')

        time.sleep(3)
        driver.get(url=url)
        time.sleep(3)

        # product_id
        product_id = driver.find_element(
            By.XPATH, '//div[contains(text(), "Артикул: ")]'
        ).text.split('Артикул: ')[1]

        page_source = str(driver.page_source)
        soup = BeautifulSoup(page_source, 'lxml')

        # временное сохранение файла страницы товара, удаляется в блоке finally
        file_path = f'product_{product_id}.html'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page_source)

        # product_name
        product_name = soup.find(
            'div', attrs={"data-widget": 'webProductHeading'}
        ).find('h1').text.strip().replace('\t', '').replace('\n', ' ')

        # product statistic
        try:
            product_statistic = soup.find(
                'div', attrs={"data-widget": 'webSingleProductScore'}
            ).text.strip()

            if " • " in product_statistic:
                product_stars, product_reviews = map(str.strip, product_statistic.split(' • '))
            else:
                product_stars, product_reviews = None, None
        except:
            product_statistic = product_stars = product_reviews = None

        # product price
        product_ozon_card_price = None
        product_discount_price = None
        product_base_price = None

        try:
            # Попытка найти цену с Ozon Картой
            ozon_card_price_element = soup.find('span', string="c Ozon Картой")
            if ozon_card_price_element:
                product_ozon_card_price = ozon_card_price_element.parent.find('div').find('span').text.strip()

            # Попытка найти обычные цены
            price_element = soup.find('span', string="без Ozon Карты")
            if price_element:
                price_spans = price_element.parent.parent.find('div').findAll('span')
                product_discount_price = price_spans[0].text.strip() if len(price_spans) > 0 else None
                product_base_price = price_spans[1].text.strip() if len(price_spans) > 1 else None
            else:
                # Если нет цен с Ozon Картой, ищем стандартные цены
                price_div = soup.find('div', attrs={"data-widget": 'webPrice'})
                if price_div:
                    price_spans = price_div.findAll('span')
                    product_discount_price = price_spans[0].text.strip() if len(price_spans) > 0 else None
                    product_base_price = price_spans[1].text.strip() if len(price_spans) > 1 else None

        except Exception as e:
            print(f"[-] Ошибка при получении цен: {e}")

        # Очистка от ₽ и пробелов
        def clean_price(value):
            return value.replace("₽", "").replace(" ", "").strip() if value else None

        product_ozon_card_price = clean_price(product_ozon_card_price)
        product_discount_price = clean_price(product_discount_price)
        product_base_price = clean_price(product_base_price)

        # Очистка product_reviews от ненужных символов
        if product_reviews:
            product_reviews = (product_reviews.replace(" ", "")
                               .replace("отзыв", "").replace("а", "").replace("ов", "").strip())

        product_data = {
            'product_id': product_id, # Артикул
            'name': product_name,
            'link': url,
            'seller_id': None,
            'date_receipt': date_receipt, # Дата и время сбора данных
            'ozon_card_price': product_ozon_card_price,
            'discount_price': product_discount_price,
            'base_price': product_base_price,
            'star_count': product_stars,
            'review_count': product_reviews
        }

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return product_data
    except Exception as e:
        error_msg = (
            f"[-] Ошибка в collect_product_info\n"
            f"\tURL: {url}\n"
            f"\tТип ошибки: {type(e).__name__}\n"
            f"\tОписание: {str(e)}\n"
        )
        print(error_msg)
        return None
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# преобразование данных для загрузки в БД
async def prepare_data_for_db(products_data, product_service):
    products_to_create = []
    products_data_to_create = []

    for item in products_data:

        product_id = await product_service.get_product_name(item['product_id'])
        if not product_id:
            product = Product(
                id=int(item['product_id']),
                name=item['name'],
                link=item['link'],
                seller_id=None
            )
            products_to_create.append(product)

        # Преобразование цен из строк в float (если они не None)
        ozon_card_price = float(item['ozon_card_price']) if item['ozon_card_price'] is not None else None
        discount_price = float(item['discount_price']) if item['discount_price'] is not None else None
        base_price = float(item['base_price']) if item['base_price'] is not None else None

        # Преобразование звезд и отзывов
        star_count = float(item['star_count']) if item['star_count'] is not None else None
        review_count = int(item['review_count']) if item['review_count'] is not None else None

        # Создание объекта ProductData
        product_data = ProductData(
            product_id=int(item['product_id']),
            date_receipt=datetime.strptime(item['date_receipt'], "%Y-%m-%d %H:%M:%S"),
            ozon_card_price=ozon_card_price,
            discount_price=discount_price,
            base_price=base_price,
            star_count=star_count,
            review_count=review_count
        )

        products_data_to_create.append(product_data)

    return products_to_create, products_data_to_create

# сохранение данных в БД
async def save_to_database(products_to_create: list[Product], products_data_to_create: list[ProductData]):
    async with get_async_session() as session:
        try:
            # Вставляем продукты, пропуская дубликаты
            for product in products_to_create:
                try:
                    session.add(product)
                    await session.flush()
                except IntegrityError:
                    await session.rollback()
                    print(f"Товар с артикулом {product.id} уже существует, пропуск...")

            # Вставляем данные продуктов
            for product_data in products_data_to_create:
                try:
                    session.add(product_data)
                    await session.flush()
                except IntegrityError as e:
                    await session.rollback()
                    print(f"Ошибка при вставке данных товара для товара с артикулом {product.id}: {e}")

            await session.commit()
            print("[+] Данные успешно сохранены в базу данных")
        except Exception as e:
            await session.rollback()
            print(f"[!] Ошибка при сохранении в базу данных: {e}")
            raise
        finally:
            await session.close()