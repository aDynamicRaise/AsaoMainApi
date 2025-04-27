
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from database import get_async_session, Product, ProductData
from utils.repository import AbstractRepository


class ProductService:
    def __init__(self, repo: AbstractRepository):
        self.repo: type[AbstractRepository] = repo

    async def get_product_name(self, product_id: int) -> str | None:
        return await self.repo.get_name_by_id(product_id)

    async def get_product_id(self, product_id: int) -> str | None:
        return await self.repo.get_id_by_id(product_id)


    # преобразование данных для загрузки в БД
    async def prepare_data_for_db(self, products_data):
        products_to_create = []
        products_data_to_create = []

        for item in products_data:

            product_name = await self.get_product_name(int(item['product_id']))
            if not product_name:
                product = Product(
                    id=int(item['product_id']),
                    name=item['name'],
                    link=item['link'],
                    seller_id=item['seller_id']
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
    async def save_to_database(self, products_to_create: list[Product], products_data_to_create: list[ProductData]):
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

                    # Проверка существование продукта
                    exists = await session.get(Product, product_data.product_id)
                    if not exists:
                        print(f"Продукт {product_data.product_id} не найден, пропуск")
                        continue
                    
                    try:
                        session.add(product_data)
                        await session.flush()
                    except IntegrityError as e:
                        await session.rollback()
                        print(f"Ошибка при вставке данных товара с артикулом {product.id}: {e}")
                        raise e

                await session.commit()
                print("[+] Данные успешно сохранены в базу данных")
            except Exception as e:
                await session.rollback()
                print(f"[!] Ошибка при сохранении в базу данных: {e}")
                raise e
            finally:
                await session.close()