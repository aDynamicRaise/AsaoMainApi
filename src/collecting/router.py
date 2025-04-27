from fastapi import APIRouter, Depends
from collecting.schemas import ProductBase, ProductLink
from collecting.services import ProductService
from collecting.dependencies import product_service
from typing import Annotated
from datetime import datetime
from config import msk_timezone
import requests

router = APIRouter(tags=["collecting"])


#Сбор данных по товару (на основе product_id в request) и его конкурентам и сохранение данных в БД
@router.post("/update_product_data")
async def update_product_data(
    product_service: Annotated[ProductService, Depends(product_service)],
    request: ProductLink = Depends(),
):
    try:
        # Получаем имя продукта по ID
        # product_name = await product_service.get_product_name(request.product_id)
        # if not product_name:
        #     return {'status': 'error', 'message': f'Товар с артикулом {request.product_id} не найден.'}

        # дата и время сбора данных
        date_receipt = datetime.now(msk_timezone).strftime("%Y-%m-%d %H:%M:%S")  # Пример: 2025-04-25 15:30:45

        # Получаем данные по товарам
        # products_data = await product_service.get_products_data(product_name, 10, date_receipt)       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        products_data = requests.get(f"http://host.docker.internal:8000/collecting/products_json?product_url={request.product_link}&seller_id={request.seller_id}").json()

        if not products_data:
            return {'status': 'error', 'message': f'Не удалось собрать данные по товару с артикулом {request.product_id} и его конкурентам.'}

        # Преобразуем данные для загрузки в БД
        products_to_create, products_data_to_create = await product_service.prepare_data_for_db(products_data)

        # Сохраняем в базу данных
        await product_service.save_to_database(products_to_create, products_data_to_create)

        return {"message" : f"Новые данные успешно собраны", "status" : 200}
    except Exception as e:
        error_msg = (
            f"[-] Ошибка в update_product_data\n"
            f"\tТип ошибки: {type(e).__name__}\n"
            f"\tОписание: {str(e)}\n"
        )
        print(error_msg)
        raise e
        return {'status': 'error', 'message': str(e)}