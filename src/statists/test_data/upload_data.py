
import time
from datetime import datetime
import json
import random

from sqlalchemy.exc import IntegrityError

from database import get_async_session
from database import Product, ProductData


import os


def load_data_from_json():
    with open("statistics/test_data/test_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

    products = []
    products_data = []
    back_id = 0

    for item in data:
        # Создание объекта Product
        if item['id'] != back_id:
            product = Product(
                id=int(item['id']),
                name=item['name'],
                link=item['link'],
                seller_id=1
            )
        
        # Преобразование цен из строк в float (если они не None)
        ozon_card_price = float(item['ozon_card_price']) if item['ozon_card_price'] is not None else 0.0
        discount_price = float(item['discount_price']) if item['discount_price'] is not None else None
        base_price = float(item['base_price'])
        
        # Создание объекта ProductData
        product_data = ProductData(
            product_id=int(item['id']),
            date_receipt=datetime.now(),
            ozon_card_price=ozon_card_price,
            discount_price=discount_price,
            base_price=base_price,
            star_count=float(item['stars']),
            review_count=int(item['reviews'])
        )
        time.sleep(random.randrange(2, 5))
        products.append(product)
        products_data.append((product, product_data))  # Сохраняем пару (Product, ProductData)
        back_id = item['id']

    return products, products_data





async def save_to_database(products: list[Product], products_data_pairs: list[tuple[Product, ProductData]]):
    async with get_async_session() as session:
        try:
            # Вставляем продукты
            session.add_all(products)
            await session.flush()  # Получаем сгенерированные ID
            
            # Теперь создаем ProductData с этими же product_id
            products_data = []
            for product, product_data in products_data_pairs:
                product_data.product_id = product.id
                products_data.append(product_data)
            
            # Вставляем данные продуктов
            session.add_all(products_data)
            await session.commit()
            print("Данные успешно сохранены в базу данных")
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()



async def main():
    print("Current Working Directory:", os.getcwd())
    products, products_data_pairs = load_data_from_json()
    
    # Вывод для проверки
    print("Products:")
    for product in products:
        print(f"Name: {product.name}, Link: {product.link}, Seller ID: {product.seller_id}")
    
    print("\nProducts Data:")
    for product, product_data in products_data_pairs:
        print(f"Product ID: {product.id} (will be set after insert), "
              f"Base Price: {product_data.base_price}, "
              f"Stars: {product_data.star_count}")
    
    await save_to_database(products, products_data_pairs)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())