from sqlalchemy import select

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


from database.models import User


async def get_all_users(session: AsyncSession):
        query = select(User).order_by(User.id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records


async def add_one_user(session: AsyncSession, **values):
        new_instance = User(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance


async def get_id_by_login(login: str, password: str, session: AsyncSession):
    query = select(User.id).filter_by(login=login, password=password)
    result = await session.execute(query)
    records = result.scalars().first()
    return records


async def get_current_user(payload: dict, session: AsyncSession):
    user_id = int(payload.get("sub"))
    return await get_user_by_id(user_id, session=session)



async def get_user_by_id(id: int, session: AsyncSession):
        query = select(User).filter_by(id=id)
        result = await session.execute(query)
        # records = result.scalar_one_or_none()
        records = result.scalars().first()
        
        return records
