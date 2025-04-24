from sqlalchemy import select
from database.connection import get_async_session
from database.db_helper import db_helper
from database.models import Product
from utils.repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    @classmethod
    async def get_name_by_id(cls, product_id: int) -> str | None:
        async with db_helper.session_getter() as session:
            stmt = select(cls.model.name).filter_by(id=product_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_id_by_id(cls, product_id: int) -> str | None:
        async with db_helper.session_getter() as session:
            stmt = select(cls.model.id).filter_by(id=product_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()