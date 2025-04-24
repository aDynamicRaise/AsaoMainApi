from fastapi import APIRouter, Depends
from collecting.schemas import ProductBase
from collecting.services import ProductService, get_products_data, prepare_data_for_db, save_to_database
from collecting.dependencies import product_service
from typing import Annotated
from datetime import datetime

router = APIRouter(tags=["collecting"])

#Сбор данных по товару (на основе product_id в request) и его конкурентам
@router.post("/update_product_data")
async def update_product_data(
    product_service: Annotated[ProductService, Depends(product_service)],
    request: ProductBase = Depends(),
):
    try:
        # Получаем имя продукта по ID
        product_name = await product_service.get_product_name(request.product_id)
        if not product_name:
            return {'status': 'error', 'message': f'Товар с артикулом {request.product_id} не найден.'}

        # дата и время сбора данных
        date_receipt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Пример: 2025-04-25 15:30:45

        # Получаем данные по товарам
        products_data = await get_products_data(product_name, 10, date_receipt)

        # Преобразуем данные для загрузки в БД
        products_to_create, products_data_to_create = await prepare_data_for_db(products_data, product_service)

        # Сохраняем в базу данных
        await save_to_database(products_to_create, products_data_to_create)

        return {"message" : f"Новые данные успешно собраны. Дата сбора: {date_receipt}", "status" : 200}
    except Exception as e:
        error_msg = (
            f"[-] Ошибка в update_product_data\n"
            f"\tТип ошибки: {type(e).__name__}\n"
            f"\tОписание: {str(e)}\n"
        )
        print(error_msg)
        return {'status': 'error', 'message': str(e)}