
from pydantic import EmailStr
from sqlalchemy import select
from database.connection import get_async_session
from database.db_helper import db_helper
from database.models import User, UserPasses
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    @classmethod
    async def get_id_by_email(self, email: str) -> int | None:
        async with db_helper.session_getter() as session:
            stmt = select(self.model.id).filter_by(email=email)
            result = await session.execute(stmt)
            result = result.scalars().first()
            return result
    
    @classmethod
    async def get_name_by_id(self, user_id: int) -> int | None:
        async with db_helper.session_getter() as session:
            stmt = select(self.model.name).filter_by(id=user_id)
            result = await session.execute(stmt)
            result = result.scalars().first()
            return result

class UserPassRepository(SQLAlchemyRepository):
    model = UserPasses

    @classmethod
    async def get_hash_by_id(self, user_id: int) -> str | None:
        async with db_helper.session_getter() as session:
            stmt = select(self.model.hash_pass).filter_by(user_id=user_id).order_by(UserPasses.date_pass.desc()).limit(1)
            result = await session.execute(stmt)
            result = result.scalars().first()
            return result